from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bcrypt = Bcrypt()

def create_app():
    """Factory function to create the Flask app."""
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')  # Ensure 'Config' class is set up in config.py

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)

	# import and register blueprints
    from .routes.supplements_routes import supplements
    from .routes.notification_routes import notifications
    from app.routes.mother_route import mother_bp
    from app.routes.antenatal_route import antenatal_bp
    from app.routes.hospital_route import hospital_bp
    

    app.register_blueprint(supplements)
    app.register_blueprint(notifications)
    app.register_blueprint(mother_bp)
    app.register_blueprint(antenatal_bp)
    app.register_blueprint(hospital_bp)
    
   
    return app
