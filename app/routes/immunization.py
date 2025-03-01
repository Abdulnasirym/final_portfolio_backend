from flask import Blueprint, request, jsonify, flash, json
from app.models.children import Children  
from app.models.mother_model import Mother
from app.models.immunization import Immunization
from app import db 
from datetime import datetime

immunization = Blueprint('immunization', __name__)

@immunization.route('/add_immunization', methods=['GET', 'POST'])
def add_immunization():
    if request.method == 'POST':
        # Retrieve form data
        parent_id = request.form.get('parent_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        previous_date = request.form.get('previous_date')
        next_date = request.form.get('next_date')
        weight = request.form.get('weight')
        injections = request.form.get('injections')

        # Validate required fields
        if any(not field for field in [first_name, last_name, age, previous_date, next_date, weight, injections]):
            flash("Please add the required information.")
            return jsonify({'message': 'Please add the required information'})

        try:
            # Convert dates to Python date objects
            previous_date = datetime.strptime(previous_date, "%Y-%m-%d").date()
            next_date = datetime.strptime(next_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        # Convert injections to JSON list
        injections_list = [injection.strip() for injection in injections.split(",")]

        parent = Mother.query.filter_by(id=parent_id).first()
        child = Children.query.filter_by(children_id = children_id).first()

        if not parent or not child:
            return jsonify({'message': 'Parent or child not found'}), 404

        new_immunization = Immunization(
            first_name=first_name,
            last_name=last_name,
            parent_id=parent.id,
            children_id=child.children_id,
            parent_first_name=parent.first_name,
            parent_last_name=parent.last_name,
            injections=json.dumps(injections_list),
            weight=weight,
            age=age,
            previous_date=previous_date,
            next_date=next_date
        )

        # Add to database
        db.session.add(new_immunization)
        db.session.commit()

        flash("Immunization schedule added.")
        return jsonify({"message": "Immunization Schedule added"})

@immunization.route('/get_immunization', methods=['GET'])
def get_immunizations(children_id):
    immunizations = Immunization.query.all()  
    
    result = []  

    for immunization in immunizations:  # Iterate over the list
        result.append({ 
            "full_name": f"{immunization.first_name} {immunization.last_name}",  # Combining first and last names
            "parent_name": f"{immunization.parent_first_name} {immunization.parent_last_name}",
            "injections": json.loads(immunization.injections),  # Convert JSON string back to list
            "weight": immunization.weight,
            "age": immunization.age,
            "previous_date": immunization.previous_date.strftime("%Y-%m-%d"),
            "next_date": immunization.next_date.strftime("%Y-%m-%d")
        })

    return jsonify(result), 200

@immunization.route('/get_immunization_details/<string:immunization_id>', methods=['GET'])
def get_immunization_details(immunization_id):
    immunization = Immunization.query.get_or_404(immunization_id)
    
    return jsonify({
       "full_name": f"{immunization.first_name} {immunization.last_name}",  
            "parent_name": f"{immunization.parent_first_name} {immunization.parent_last_name}",
            "injections": json.loads(immunization.injections),  # Convert JSON string back to list
            "weight": immunization.weight,
            "age": immunization.age,
            "previous_date": immunization.previous_date.strftime("%Y-%m-%d"),
            "next_date": immunization.next_date.strftime("%Y-%m-%d")
    }), 200

@immunization.route('/update_immunization/<string:immunization_id>', methods=['PUT'])
def update_details(immunization_id):
    data = request.json

    # Query the database for the immunization record
    details = Immunization.query.get_or_404(immunization_id)
    if not details:
        return jsonify({"error": "Details do not exist"}), 404

    # Update the record fields
    details.first_name = data.get('first_name', details.first_name)
    details.last_name = data.get('last_name', details.last_name)
    details.parent_first_name = data.get('parent_first_name', details.parent_first_name)
    details.parent_last_name = data.get('parent_last_name', details.parent_first_name)
    details.injections = json.dumps(data.get('injections', json.loads(details.injections)))  # Handle JSON conversion
    details.weight = data.get('weight', details.weight)
    details.age = data.get('age', details.age)

    # Convert and validate dates
    try:
        if 'previous_date' in data:
            details.previous_date = datetime.strptime(data['previous_date'], '%Y-%m-%d').date()
        if 'next_date' in data:
            details.next_date = datetime.strptime(data['next_date'], '%Y-%m-%d').date()
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {str(e)}. Use YYYY-MM-DD."}), 400

    # Save the changes to the database
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    # Return a success response
    return jsonify({"message": "Data successfully updated"}), 200

@immunization.route('/delete_immunization/<string:immunization_id>', methods=['DELETE', 'GET', 'POST'])
def delete_immunization(immunization_id):
    immunization = Immunization.query.get(immunization_id)  # Using get() instead of get_or_404()

    if not immunization:
        return jsonify({"error": "Record does not exist"}), 404  # Return error response if not found

    db.session.delete(immunization)
    db.session.commit()

    return jsonify({"message": "Record Deleted"})


