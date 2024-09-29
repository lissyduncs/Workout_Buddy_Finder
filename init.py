from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()  # Initialide bcrypt for password hashing
jwt = JWTManager()  # Initialise JWT for handling authentication

# Function to initialise the extensions
def init_app(app):
    bcrypt.init_app(app)
    jwt.init_app(app)