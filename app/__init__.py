from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
	app = Flask(__name__)


	# Load cnfigurations
	app.config.from_object('config.Config')

	# Initialize the extensions
	db.init_app(app)
	migrate.init_app(app, db)
	mail.init_app(app)

	# import and register blueprints
	
	from .routes.supplements_routes import supplements
	from .routes.notification_routes import notifications

	app.register_blueprint(supplements)
	app.register_blueprint(notifications)

	return app	