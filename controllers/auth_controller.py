from flask import Blueprint, request
from models.user import User, user_schema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token
from datetime import timedelta

# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Route for user registration
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # Extract data from the request body
        body_data = request.get_json()

        # Create a new User instance with provided name and email
        user = User(
            user_name=body_data.get("user_name"),
            user_email=body_data.get("user_email")
        )

        # Hash the provided password
        password = body_data.get("user_password")
        if password:
            user.user_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Save the new user in the database
        db.session.add(user)
        db.session.commit()

        # Return the newly created user information (excluding the password)
        return user_schema.dump(user), 201

    except IntegrityError as err:
        # Handle NOT NULL violation (e.g., missing required fields)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        # Handle unique constraint violation (e.g., duplicate email)
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400

# Route for user login
@auth_bp.route("/login", methods=["POST"])
def login_user():
    # Extract data from the request body
    body_data = request.get_json()

    # Query the database for the user by their email
    stmt = db.select(User).filter_by(user_email=body_data.get("user_email"))
    user = db.session.scalar(stmt)

    # Check if user exists and the password is correct
    if user and bcrypt.check_password_hash(user.user_password, body_data.get("user_password")):
        # Generate a JWT token for the user with a 1-day expiration
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))

        # Return the token and user information (excluding password)
        return {"user_email": user.user_email, "token": token}
    
    else:
        # If the user doesn't exist or the password is incorrect, return an error
        return {"error": "Invalid email or password"}, 400