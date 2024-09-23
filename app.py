from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from init import bcrypt, jwt, init_app

from controllers.buddy_request_controller import buddy_request_bp
app.register_blueprint(buddy_request_bp)

from controllers.workout_session_controller import workout_session_bp
app.register_blueprint(workout_session_bp)

from controllers.message_controller import message_bp
app.register_blueprint(message_bp)

# Initialise the extensions
init_app(app)

app = Flask(__name__)

# Configure the database URL and initialse SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_buddy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Users, Workout Sessions, Buddy Requests
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_location = db.Column(db.String(100), nullable=True)

class WorkoutSession(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    workout_location = db.Column(db.String(100), nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)
    workout_time = db.Column(db.String(100), nullable=False)

class BuddyRequest(db.Model):
    buddy_request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_session.workout_id'), nullable=False)
    request_message = db.Column(db.String(255), nullable=True)

# Endpoint to create a user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
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

# Endpoint to create a workout session
@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        new_workout = WorkoutSession(
            customer_id=data['customer_id'],
            workout_location=data['workout_location'],
            workout_type=data['workout_type'],
            workout_time=data['workout_time']
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({'message': 'Workout session created successfully!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during workout session creation'}), 500

# Endpoint to create a buddy request
@app.route('/requests', methods=['POST'])
def create_buddy_request():
    try:
        data = request.get_json()
        new_request = BuddyRequest(
            workout_id=data['workout_id'],
            request_message=data.get('request_message')
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Buddy request created successfully!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during buddy request creation'}), 500

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        result = []
        for user in users:
            user_data = {
                'user_id': user.user_id,
                'user_name': user.user_name,
                'user_email': user.user_email,
                'user_location': user.user_location
            }
            result.append(user_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching users'}), 500

# Endpoint to get all of the workout sessions
@app.route('/workouts', methods=['GET'])
def get_workouts():
    try:
        workouts = WorkoutSession.query.all()
        result = []
        for workout in workouts:
            workout_data = {
                'workout_id': workout.workout_id,
                'customer_id': workout.customer_id,
                'workout_location': workout.workout_location,
                'workout_type': workout.workout_type,
                'workout_time': workout.workout_time
            }
            result.append(workout_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching workouts'}), 500

# Endpoint to get all buddy requests
@app.route('/requests', methods=['GET'])
def get_buddy_requests():
    try:
        requests = BuddyRequest.query.all()
        result = []
        for buddy_request in requests:
            request_data = {
                'buddy_request_id': buddy_request.buddy_request_id,
                'workout_id': buddy_request.workout_id,
                'request_message': buddy_request.request_message
            }
            result.append(request_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching buddy requests'}), 500

# Endpoint to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully!'}), 200
        else:
            return jsonify({'error': 'User not found!'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred during user deletion'}), 500

# Initialise the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)