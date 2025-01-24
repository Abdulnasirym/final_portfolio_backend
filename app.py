from app import create_app, db
from app.models.children import Children
from app.models.immunization import Immunization
from app.models.mothers import Mothers
target_metadata = db.metadata

app = create_app()

with app.app_context():
    # Example query
    children = Children.query.all()
    print(children)


if __name__ == "__main__":
	app.run(debug=True)
