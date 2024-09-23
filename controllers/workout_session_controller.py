from flask import Blueprint, request, jsonify
from models import WorkoutSession, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

workout_session_bp = Blueprint('workout_session', __name__, url_prefix='/workout_sessions')

# POST /workout_sessions - Create a new workout session
@workout_session_bp.route('/', methods=['POST'])
@jwt_required()
def create_workout_session():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Create a new WorkoutSession
    new_workout = WorkoutSession(
        customer_id=user_id,
        workout_location=data.get('workout_location'),
        workout_type=data.get('workout_type'),
        workout_time=datetime.strptime(data.get('workout_time'), '%Y-%m-%d %H:%M:%S')
    )
    
    db.session.add(new_workout)
    db.session.commit()

    return jsonify({
        'message': 'Workout session created successfully!',
        'workout_session': {
            'workout_id': new_workout.workout_id,
            'workout_location': new_workout.workout_location,
            'workout_type': new_workout.workout_type,
            'workout_time': new_workout.workout_time,
            'customer_id': new_workout.customer_id
        }
    }), 201

# GET /workout_sessions - Retrieve all workout sessions
@workout_session_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_workout_sessions():
    # Get all workout sessions
    workout_sessions = WorkoutSession.query.order_by(WorkoutSession.workout_time.desc()).all()
    
    result = []
    for session in workout_sessions:
        result.append({
            'workout_id': session.workout_id,
            'workout_location': session.workout_location,
            'workout_type': session.workout_type,
            'workout_time': session.workout_time,
            'customer_id': session.customer_id
        })
    
    return jsonify(result), 200

# GET /workout_sessions/<int:id> - Retrieve a specific workout session by ID
@workout_session_bp.route('/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout_session(workout_id):
    session = WorkoutSession.query.get(workout_id)
    
    if not session:
        return jsonify({'error': 'Workout session not found'}), 404
    
    return jsonify({
        'workout_id': session.workout_id,
        'workout_location': session.workout_location,
        'workout_type': session.workout_type,
        'workout_time': session.workout_time,
        'customer_id': session.customer_id
    }), 200

# PUT /workout_sessions/<int:id> - Update a workout session
@workout_session_bp.route('/<int:workout_id>', methods=['PUT'])
@jwt_required()
def update_workout_session(workout_id):
    session = WorkoutSession.query.get(workout_id)
    
    if not session:
        return jsonify({'error': 'Workout session not found'}), 404
    
    data = request.get_json()
    
    # Update the session details
    session.workout_location = data.get('workout_location', session.workout_location)
    session.workout_type = data.get('workout_type', session.workout_type)
    
    workout_time = data.get('workout_time')
    if workout_time:
        session.workout_time = datetime.strptime(workout_time, '%Y-%m-%d %H:%M:%S')

    db.session.commit()
    
    return jsonify({
        'message': 'Workout session updated successfully!',
        'workout_session': {
            'workout_id': session.workout_id,
            'workout_location': session.workout_location,
            'workout_type': session.workout_type,
            'workout_time': session.workout_time,
            'customer_id': session.customer_id
        }
    }), 200

# DELETE /workout_sessions/<int:id> - Delete a workout session
@workout_session_bp.route('/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout_session(workout_id):
    session = WorkoutSession.query.get(workout_id)
    
    if not session:
        return jsonify({'error': 'Workout session not found'}), 404
    
    db.session.delete(session)
    db.session.commit()
    
    return jsonify({'message': 'Workout session deleted successfully!'}), 200