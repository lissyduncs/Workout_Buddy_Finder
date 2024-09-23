from flask import Blueprint, request, jsonify
from models import User
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Register user route
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # Get the data from the body of the request
        body_data = request.get_json()
        # Create an instance of the User model
        user = User(
            user_name=body_data.get("user_name"),
            user_email=body_data.get("user_email")
        )
        # Hash the password
        password = body_data.get("user_password")
        if password:
            user.user_password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()
        # Return acknowledgment
        return jsonify({'message': 'User registered successfully!'}), 201
    except IntegrityError as err:
        # Handle integrity errors (e.g., unique constraint violations)
        return jsonify({'error': 'Email must be unique'}), 400

# Login user route
@auth_bp.route("/login", methods=["POST"])
def login_user():
    # Get the data from the body of the request
    body_data = request.get_json()
    # Find the user by email in the database
    user = User.query.filter_by(user_email=body_data.get("user_email")).first()
    
    # Check if the user exists and password is correct
    if user and bcrypt.check_password_hash(user.user_password, body_data.get("user_password")):
        # Create a JWT token
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
        # Respond with the token
        return jsonify({
            'user_email': user.user_email,
            'token': token
        }), 200
    else:
        # Invalid credentials
        return jsonify({'error': 'Invalid email or password'}), 401