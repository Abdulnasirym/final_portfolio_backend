from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configurations
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db) 

    # Import models locally to avoid circular imports
    with app.app_context():
        from app.models.mothers import Mother
        from app.models.children import Children
        
        
 
    
    # Import and register Blueprints
    from app.routes.children import children_bp
    app.register_blueprint(children_bp,  url_prefix = '/')

    from app.routes.immunization import immunization
    app.register_blueprint(immunization, url_prefix = '/')

 
    
    return app
