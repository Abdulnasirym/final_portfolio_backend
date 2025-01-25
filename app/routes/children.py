from flask import Blueprint, request, jsonify, flash, abort
from app.models.children import Children  
from app.models.mothers import Mother
from app import db 
from werkzeug.security import generate_password_hash, check_password_hash

# Create Blueprint
children_bp = Blueprint('children', __name__)


# Defining  route
@children_bp.route('/add_child', methods=['GET', 'POST'])
def add_child():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        blood_group = request.form.get('blood_group')
        genotype = request.form.get('genotype')
        weight = request.form.get('weight')
        parent_email = request.form.get('parent_email')
        nationality = request.form.get('nationality')
        age = request.form.get('age')

        # Check for missing fields
        if any(not field for field in [first_name, last_name, blood_group, genotype, weight, nationality, age, parent_email]):
            flash("All fields are required")
            return jsonify({'message': 'All fields are required'}), 400

        # Find mother using parent_email
        mother = Mother.query.filter_by(email=parent_email).first()
        if not mother:
            flash("Mother not found")
            return jsonify({'message': 'Mother not found'}), 404

        # Create new child record
        new_child = Children(
            first_name=first_name,
            last_name=last_name,
            parent_id=mother.id,  # Reference the mother's ID
            blood_group=blood_group,
            genotype=genotype,
            weight=weight,
            parent_email=parent_email,
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
    children = Children.query.all()  # This returns a list of Children objects

    # Prepare the response data
    result = []
    for child in children:
        result.append({
            "children_id": child.children_id,
            "first_name": child.first_name,
            "last_name": child.last_name,
            "parent_id": child.parent_id,
            "blood_group": child.blood_group,
            "genotype": child.genotype,
            "weight": child.weight,
            "parent_email": child.parent_email,
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
       "id":            children.children_id,
       "first_name":    children.first_name,
       "last_name":     children.last_name,
       "parent_id":     children.parent_id,
       "blood_group":   children.blood_group,
       "genotype":      children.genotype,
       "weight":        children.weight,
       "parent_email":  children.parent_email,
       "age":           children.age,
       "nationality":   children.nationality,
       "date_added":    children.date_added,
       "date_updated":  children.date_updated

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
    children.parent_email = data.get('parent_email', children.parent_email)
    children.blood_group = data.get('blood_group', children.blood_group)
    children.genotype = data.get('genotype', children.genotype)
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

  
