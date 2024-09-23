from flask import Blueprint, request, jsonify
from models import BuddyRequest, User, WorkoutSession, db
from flask_jwt_extended import jwt_required, get_jwt_identity

buddy_request_bp = Blueprint('buddy_request', __name__, url_prefix='/buddy_requests')

# POST /buddy_requests - Create a new buddy request
@buddy_request_bp.route('/', methods=['POST'])
@jwt_required()
def create_buddy_request():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Check if workout session exists
    workout = WorkoutSession.query.get(data.get('workout_id'))
    if not workout:
        return jsonify({'error': 'Workout session not found'}), 404

    # Create a new buddy request
    new_request = BuddyRequest(
        workout_id=data['workout_id'],
        user_id=user_id,
        status=data.get('status', 'pending')  # the default status is pending
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    return jsonify({
        'message': 'Buddy request created successfully!',
        'buddy_request': {
            'buddy_request_id': new_request.buddy_request_id,
            'workout_id': new_request.workout_id,
            'user_id': new_request.user_id,
            'status': new_request.status
        }
    }), 201

# GET /buddy_requests -retrieves all the buddy requests
@buddy_request_bp.route('/', methods=['GET'])
@jwt_required()
def get_buddy_requests():
    user_id = get_jwt_identity()
    
    # Retrieve all buddy requests made by the user
    buddy_requests = BuddyRequest.query.filter_by(user_id=user_id).all()
    
    result = []
    for request in buddy_requests:
        result.append({
            'buddy_request_id': request.buddy_request_id,
            'workout_id': request.workout_id,
            'user_id': request.user_id,
            'status': request.status
        })
    
    return jsonify(result), 200

# GET /buddy_requests/<int:id> - Retrieve a specific buddy request by ID
@buddy_request_bp.route('/<int:buddy_request_id>', methods=['GET'])
@jwt_required()
def get_buddy_request(buddy_request_id):
    buddy_request = BuddyRequest.query.get(buddy_request_id)
    
    if not buddy_request:
        return jsonify({'error': 'Buddy request not found'}), 404
    
    return jsonify({
        'buddy_request_id': buddy_request.buddy_request_id,
        'workout_id': buddy_request.workout_id,
        'user_id': buddy_request.user_id,
        'status': buddy_request.status
    }), 200

# PUT /buddy_requests/<int:id> - Update a buddy request status
@buddy_request_bp.route('/<int:buddy_request_id>', methods=['PUT'])
@jwt_required()
def update_buddy_request(buddy_request_id):
    data = request.get_json()
    buddy_request = BuddyRequest.query.get(buddy_request_id)
    
    if not buddy_request:
        return jsonify({'error': 'Buddy request not found'}), 404
    
    # Update the status of the buddy request
    buddy_request.status = data.get('status', buddy_request.status)
    db.session.commit()
    
    return jsonify({
        'message': 'Buddy request updated successfully!',
        'buddy_request': {
            'buddy_request_id': buddy_request.buddy_request_id,
            'workout_id': buddy_request.workout_id,
            'user_id': buddy_request.user_id,
            'status': buddy_request.status
        }
    }), 200

# DELETE /buddy_requests/<int:id> - delete a buddy request
@buddy_request_bp.route('/<int:buddy_request_id>', methods=['DELETE'])
@jwt_required()
def delete_buddy_request(buddy_request_id):
    buddy_request = BuddyRequest.query.get(buddy_request_id)
    
    if not buddy_request:
        return jsonify({'error': 'Buddy request not found'}), 404
    
    db.session.delete(buddy_request)
    db.session.commit()
    
    return jsonify({'message': 'Buddy request deleted successfully!'}), 200