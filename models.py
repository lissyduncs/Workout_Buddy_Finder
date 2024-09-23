from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)
    user_location = db.Column(db.String(120))

    # Relationships
    workout_sessions = db.relationship('WorkoutSession', backref='user', lazy=True)
    buddy_requests = db.relationship('BuddyRequest', backref='user', lazy=True)
    messages = db.relationship('Message', backref='user', lazy=True)

# Define the WorkoutSession model
class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    workout_location = db.Column(db.String(120), nullable=False)
    workout_type = db.Column(db.String(120), nullable=False)
    workout_time = db.Column(db.DateTime, nullable=False)

# Define the BuddyRequest model
class BuddyRequest(db.Model):
    __tablename__ = 'buddy_requests'
    buddy_request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.workout_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')

# Define the Message model
class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    buddy_request_id = db.Column(db.Integer, db.ForeignKey('buddy_requests.buddy_request_id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)