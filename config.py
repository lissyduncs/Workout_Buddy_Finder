import os

class Config:
    # Secret key for security 
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///workout_buddy.db'
    
    # Disable tracking modifications 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask environment 
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    
    # Debug mode 
    DEBUG = True if FLASK_ENV == 'development' else False

    # SQLAlchemy echo - debugging 
    SQLALCHEMY_ECHO = True if FLASK_ENV == 'development' else False

    # Allowing database migrations 
    MIGRATE_ENABLED = True
