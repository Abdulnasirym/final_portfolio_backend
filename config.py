import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'promiseperpetuaabdulnasircole')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
