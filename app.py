from app import create_app, db
from flask_migrate import upgrade

app = create_app()

# Migrate database schema
with app.app_context():
    # Apply migrations if necessary
    upgrade()  # This is to apply migrations, using Flask-Migrate.

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # You can make port configurable with an environment variable
