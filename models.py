from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the User model that represents users in the system
# Table stores the important user information.
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    user_name = db.Column(db.String(80), nullable=False)  # user's name
    user_email = db.Column(db.String(120), unique=True, nullable=False)  # unique email
    user_password = db.Column(db.String(120), nullable=False)  # stores the hashed password
    user_location = db.Column(db.String(120))  # user location and can be optional
    
    # Relationships to the other models
    workout_sessions = db.relationship('WorkoutSession', backref='user', lazy=True)  # user to workout session one-to-many relationship
    buddy_requests = db.relationship('BuddyRequest', backref='user', lazy=True)  # user tombuddy request one-to-many
    messages = db.relationship('Message', backref='user', lazy=True)  # user to messages one-to-many 

# Define the workout session model
class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary key
    customer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # foreign key linked to User
    workout_location = db.Column(db.String(120), nullable=False)  # workout session location
    workout_type = db.Column(db.String(120), nullable=False)  # workout type
    workout_time = db.Column(db.DateTime, nullable=False)  # date and time of the session

# define the buddy request model
class BuddyRequest(db.Model):
    __tablename__ = 'buddy_requests'
    buddy_request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary key
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.workout_id'), nullable=False)  # Foreign key linking to a workout session
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # foreign key linking to the user who made the request
    status = db.Column(db.String(50), nullable=False, default='pending')  # status of the request
# Define the message model
class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Foreign key linking to the sender of message
    buddy_request_id = db.Column(db.Integer, db.ForeignKey('buddy_requests.buddy_request_id'), nullable=False)  # foreign key linking to the buddy request
    content = db.Column(db.String(500), nullable=False)  # The actual content of the message
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)  # Timestamp for when the message was sent which defaults to current time