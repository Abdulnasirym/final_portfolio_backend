from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize extensions
db = SQLAlchemy()

def create_app():
	app = Flask(__name__)


	# Load cnfigurations
	app.config.from_object('config.Config')

	# Initialize the extensions
	db.init_app(app)

	# import and register blueprints

	return app	