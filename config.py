import os
from datetime import timedelta
from flask_jwt_extended import JWTManager
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Access JWT secret
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access token expires in 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token expires in 30 days
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
   