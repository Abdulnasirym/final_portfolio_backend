from flask import Blueprint, request, jsonify, flash, abort
from app.models.children import Children  
from app.models.mother_model import Mother
from app import db 
from werkzeug.security import generate_password_hash, check_password_hash

# Create Blueprint
children_bp = Blueprint('children', __name__)


# Defining  route
@children_bp.route('/add_child', methods=['POST'])
def add_child():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        weight = request.form.get('weight')
        nationality = request.form.get('nationality')
        age = request.form.get('age')

        # Check for missing fields
        if any(not field for field in [first_name, last_name,  weight, nationality, age]):
            flash("All fields are required")
            return jsonify({'message': 'All fields are required'}), 400

        # Find mother using parent_email
        mother = Mother.query.filter_by(id=mother_id).first()
        if not mother:
            flash("Mother not found")
            return jsonify({'message': 'Mother not found'}), 404

        # Create new child record
        new_child = Children(
            parent_id=parent_id,
            parent_first_name=mother.first_name,
            parent_last_name= mother.last_name,
            first_name=first_name,
            last_name=last_name,
            weight=weight,
            nationality=nationality,
            age=age
        )

        # Add to database
        db.session.add(new_child)
        db.session.commit()

        flash("Child information added successfully")
        return jsonify({'message': 'Child information added successfully'}), 201

    return jsonify({'message': 'Invalid request method'}), 405


@children_bp.route('/get_children', methods=['GET'])
def get_children():
    # Query the database for all children records
    children = Children.query.all()

    if not children:
        return jsonify({"message": "No children found for this mother"}), 404  
   
    # Prepare the response data
    result = []
    for child in children:
        result.append({
            "id": child.children_id,
            "full_name": f"{child.first_name} {child.last_name}",
            "parent_name": f"{child.parent_first_name} {child.parent_last_name}",
            "weight": child.weight,
            "age": child.age,
            "nationality": child.nationality,
            "date_added": child.date_added.strftime('%Y-%m-%d %H:%M:%S') if child.date_added else None,
            "date_updated": child.date_updated.strftime('%Y-%m-%d %H:%M:%S') if child.date_updated else None
        })

    return jsonify(result), 200


@children_bp.route('/get_details/<string:children_id>', methods=['GET'])
def get_details(children_id):

     # Query the database for the child record
    children = Children.query.get_or_404 (children_id)
   
    #Display the details
    return jsonify({
            "full_name": f"{children.first_name} {children.last_name}",
            "first_name": f"{children.first_name}",
            "last_name": f"{children.last_name}",
            "parent_name": f"{children.parent_first_name} {children.parent_last_name}",
            "weight": children.weight,
            "age": children.age,
            "nationality": children.nationality,
            "date_added": children.date_added.strftime('%Y-%m-%d %H:%M:%S') if children.date_added else None,
            "date_updated": children.date_updated.strftime('%Y-%m-%d %H:%M:%S') if children.date_updated else None

    })

@children_bp.route('/update_child/<string:children_id>', methods=['PUT'])
def update_details(children_id):
    data = request.json

    # Query the database for the child record
    children = Children.query.get(children_id)

    # Check if the child exists
    if not children:
        flash('User do not exist')
        return jsonify({"message": "User do not exist"}), 404

    # Update child details
    children.first_name = data.get('first_name', children.first_name)
    children.last_name = data.get('last_name', children.last_name)
    children.weight = data.get('weight', children.weight)
    children.nationality = data.get('nationality', children.nationality)
    children.age = data.get('age', children.age)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "Data successfully updated"}), 200



@children_bp.route('/delete_children/<string:children_id>', methods=['DELETE'])
def delete_child(children_id):
    # Fetch the child record
    children = Children.query.get_or_404(children_id)

    if not children:
        flash("Child does not exist")
        return jsonify({"message": "Child does not exist"}), 404

    # Delete the child record
    db.session.delete(children)
    db.session.commit()

    flash("Child's information deleted")
    return jsonify({"message": "Child's information deleted"}), 200

  
