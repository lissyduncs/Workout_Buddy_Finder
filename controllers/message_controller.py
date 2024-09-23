from flask import Blueprint, request, jsonify
from models import Message, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

message_bp = Blueprint('message', __name__, url_prefix='/messages')

# POST /messages - Send a new message
@message_bp.route('/', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    sender_id = get_jwt_identity()

    # Create a new message
    new_message = Message(
        sender_id=sender_id,
        receiver_id=data.get('receiver_id'),
        content=data.get('content'),
        sent_at=datetime.utcnow()
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        'message': 'Message sent successfully!',
        'message_details': {
            'message_id': new_message.message_id,
            'sender_id': new_message.sender_id,
            'receiver_id': new_message.receiver_id,
            'content': new_message.content,
            'sent_at': new_message.sent_at
        }
    }), 201

# GET /messages - Retrieve all messages for the logged-in user
@message_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_messages():
    user_id = get_jwt_identity()

    # Fetch all messages where the user is the sender or receiver
    messages = Message.query.filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).order_by(Message.sent_at.desc()).all()

    result = []
    for message in messages:
        result.append({
            'message_id': message.message_id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'content': message.content,
            'sent_at': message.sent_at
        })

    return jsonify(result), 200

# GET /messages/<int:message_id> - Retrieve a specific message by ID
@message_bp.route('/<int:message_id>', methods=['GET'])
@jwt_required()
def get_message(message_id):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    return jsonify({
        'message_id': message.message_id,
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'content': message.content,
        'sent_at': message.sent_at
    }), 200

# PUT /messages/<int:message_id> - Update a message
@message_bp.route('/<int:message_id>', methods=['PUT'])
@jwt_required()
def update_message(message_id):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    data = request.get_json()

    # Update the content of the message
    message.content = data.get('content', message.content)
    
    db.session.commit()

    return jsonify({
        'message': 'Message updated successfully!',
        'message_details': {
            'message_id': message.message_id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'content': message.content,
            'sent_at': message.sent_at
        }
    }), 200

# DELETE /messages/<int:message_id> - Delete a message
@message_bp.route('/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted successfully!'}), 200