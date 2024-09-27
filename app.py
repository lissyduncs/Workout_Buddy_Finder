from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import re  
import bleach
from config import Config
from init import bcrypt, jwt, init_app

# Register theblueprints 
from controllers.buddy_request_controller import buddy_request_bp
app.register_blueprint(buddy_request_bp)

from controllers.workout_session_controller import workout_session_bp
app.register_blueprint(workout_session_bp)

from controllers.message_controller import message_bp
app.register_blueprint(message_bp)

# initialise the extensions
init_app(app)

app = Flask(__name__)

# Configure the database URL and SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_buddy.db'  # Use SQLite for local development
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking feature to save resources
db = SQLAlchemy(app)

# the email validation function to ensure valid email format
def is_valid_email(email):
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

# models for Users, workout sessions and buddy requests
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary key for User table
    user_name = db.Column(db.String(100), nullable=False)  # Name is required
    user_email = db.Column(db.String(100), unique=True, nullable=False)  # unique email for each user
    user_password = db.Column(db.String(100), nullable=False)  # password is required
    user_location = db.Column(db.String(100), nullable=True)  # location field is optional

class WorkoutSession(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key for the workout session
    customer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign key linking to User table
    workout_location = db.Column(db.String(100), nullable=False)  # Location of the workout
    workout_type = db.Column(db.String(100), nullable=False)  # Type of workout 
    workout_time = db.Column(db.String(100), nullable=False)  # Time of the workout

class BuddyRequest(db.Model):
    buddy_request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key for Buddy Request
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_session.workout_id'), nullable=False)  # Foreign key linking to Workout Session
    request_message = db.Column(db.String(255), nullable=True)  # message from the user is optional

# endpoint to create a new user in the database
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()  
        

        if not is_valid_email(data['user_email']):
            return jsonify({'error': 'Invalid email format'}), 400

        # Create a new Userand add it to the database
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_password=data['user_password'],
            user_location=data.get('user_location')  
        )
        db.session.add(new_user)  
        db.session.commit()  
        return jsonify({'message': 'User created successfully!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400  
    except Exception as e:
        return jsonify({'error': 'An error occurred during user creation'}), 500  

# Endpoint to create a new workout session
@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        
        # Create a new Workout session  and add it to the database
        new_workout = WorkoutSession(
            customer_id=data['customer_id'],  
            workout_location=data['workout_location'],
            workout_type=data['workout_type'],
            workout_time=data['workout_time']
        )
        db.session.add(new_workout)  # Add workout session to the session 
        db.session.commit()  # save the workout session
        return jsonify({'message': 'Workout session created successfully!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400  
    except Exception as e:
        return jsonify({'error': 'An error occurred during workout session creation'}), 500  

# Endpoint to create a buddy request to join a workout session
@app.route('/requests', methods=['POST'])
def create_buddy_request():
    try:
        data = request.get_json()
        
        # Create a new Buddy request object with sanitized message
        new_request = BuddyRequest(
            workout_id=data['workout_id'],  # link to the workout session
            request_message=bleach.clean(data.get('request_message'))  
        )
        db.session.add(new_request)  # Add buddy request to the session (staged for database insertion)
        db.session.commit()  # save the buddy request
        return jsonify({'message': 'Buddy request created successfully!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400  
    except Exception as e:
        return jsonify({'error': 'An error occurred during buddy request creation'}), 500  

# Endpoint to retrieve all users from the database
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()  # Query the database to get all users
        result = []
        for user in users:
            # Map user object to a dictionary to return as JSON
            user_data = {
                'user_id': user.user_id,
                'user_name': user.user_name,
                'user_email': user.user_email,
                'user_location': user.user_location
            }
            result.append(user_data)  # Append each user to the result list
        return jsonify(result), 200  # Return the list of users with HTTP 200 status
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching users'}), 500  

# Endpoint to retrieve all workout sessions from the database
@app.route('/workouts', methods=['GET'])
def get_workouts():
    try:
        workouts = WorkoutSession.query.all()  # Query the database to get all workout sessions
        result = []
        for workout in workouts:
            # Map workout session to a dictionary to return as JSON
            workout_data = {
                'workout_id': workout.workout_id,
                'customer_id': workout.customer_id,
                'workout_location': workout.workout_location,
                'workout_type': workout.workout_type,
                'workout_time': workout.workout_time
            }
            result.append(workout_data)  # Append each workout to the result list
        return jsonify(result), 200  # Return the list of workout sessions with HTTP 200 status
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching workouts'}), 500  

# Endpoint to retrieve all buddy requests from the database
@app.route('/requests', methods=['GET'])
def get_buddy_requests():
    try:
        requests = BuddyRequest.query.all()  # Query the database to get all buddy requests
        result = []
        for buddy_request in requests:
            # Map buddy request object to a dictionary to return as JSON
            request_data = {
                'buddy_request_id': buddy_request.buddy_request_id,
                'workout_id': buddy_request.workout_id,
                'request_message': buddy_request.request_message
            }
            result.append(request_data)  # Append each buddy request to the result list
        return jsonify(result), 200  # Return the list of buddy requests with HTTP 200 status
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching buddy requests'}), 500  
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)  # Query the database to find the user by ID
        if user:
            db.session.delete(user)  # Mark the user to delete
            db.session.commit()  # delete the user
            return jsonify({'message': 'User deleted successfully!'}), 200
        else:
            return jsonify({'error': 'User not found!'}), 404  # user is not found
    except Exception as e:
        return jsonify({'error': 'An error occurred during user deletion'}), 500  

# Initialise the database and create tables
with app.app_context():
    db.create_all()  