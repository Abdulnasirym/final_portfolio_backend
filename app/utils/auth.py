from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

def hash_password(password):
    """Hash a plain-text password."""
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """Verify if the plain-text password matches the hashed password."""
    return check_password_hash(hashed_password, password)

def generate_token(user_id):
    """Generate a JWT token with a 24-hour expiry."""
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow(),  # Issued at time
        'sub': user_id  # Subject (user ID)
    }
    secret_key = current_app.config.get('SECRET_KEY')
    if not secret_key:
        raise ValueError("SECRET_KEY is not configured in the Flask app.")

    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_token(token):
    """Decode the JWT token and extract the user ID."""
    try:
        secret_key = current_app.config['SECRET_KEY']
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['sub']  # Return the user ID from the token
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}  # More informative message
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}  # More informative message
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}  # Catch other potential errors
