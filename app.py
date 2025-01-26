from dotenv import load_dotenv
from app import create_app, db
from flask_migrate import upgrade
from flask_jwt_extended import JWTManager

load_dotenv()

app = create_app()

#initializing jwt
jwt = JWTManager(app)


# Migrate database schema
with app.app_context():
    # Apply migrations if necessary
    upgrade()  # This is to apply migrations, using Flask-Migrate.

from app import create_app, db
from app.models.children import Children
from app.models.immunization import Immunization
from app.models.mother_model import Mother
target_metadata = db.metadata

app = create_app()

with app.app_context():
    # Example query
    children = Children.query.all()
    print(children)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # You can make port configurable with an environment variable
