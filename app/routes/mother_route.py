from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models.mother_model import Mother

mother_bp = Blueprint('mother_bp', __name__)

# Mother Registration
@mother_bp.route('/register_mother', methods=['GET', 'POST'])
def register_mother():
    data = request.get_json()

    # Extract fields from request data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    genotype = data.get('genotype')
    blood_group = data.get('blood_group')
    nationality = data.get('nationality')
    email = data.get('email')
    password = data.get('password')
    hospital_id = data.get('hospital_id')

    # Validate required fields
    if any(not field for field in [first_name, last_name, age, genotype, blood_group, nationality, email, password, hospital_id]):
        return jsonify({"error": "All fields are required"}), 400

    # Check if email already exists
    if Mother.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Save the new mother to the database
    new_mother = Mother(
        first_name=first_name,
        last_name=last_name,
        age=age,
        genotype=genotype,
        blood_group=blood_group,
        nationality=nationality,
        email=email,
        password_hash=password_hash,
        hospital_id=hospital_id
    )
    db.session.add(new_mother)
    db.session.commit()

    return jsonify({"message": "Mother registered successfully"}), 200


# Mother Login
@mother_bp.route('/login_mother', methods=['GET', 'POST'])
def login_mother():
    data = request.get_json()

    # Extract fields from request data
    email = data.get('email')
    password = data.get('password')

    # Validate email and password
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if the mother exists using email
    mother = Mother.query.filter_by(email=email).first()
    print(mother)

    if not mother or not check_password_hash(mother.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 400

    # Generate JWT token
    token = create_access_token(identity=mother.id)
    #return jsonify({"token": token}), 200
    return jsonify({
    'message': 'logged in successfully',
    "token": token,
    "user": {
        "id": mother.id,
        "full_name": f"{mother.first_name} {mother.last_name}",
        "email": mother.email,
        "age": mother.age,
        "blood_group": mother.blood_group,
        "genotype": mother.genotype,
        "nationality": mother.nationality,
        "hospital_id": mother.hospital_id
    }
}), 200

# Update Mother
@mother_bp.route('/update_mother/<string:mother_id>', methods=['PUT'])
def update_mother(mother_id):
    data = request.get_json()

    # Find the mother by ID
    mother = Mother.query.get(mother_id)
    if not mother:
        return jsonify({"error": "Mother not found"}), 404

    # Update fields if provided
    mother.first_name = data.get('first_name', mother.first_name)
    mother.last_name = data.get('last_name', mother.last_name)
    mother.age = data.get('age', mother.age)
    mother.genotype = data.get('genotype', mother.genotype)
    mother.blood_group = data.get('blood_group', mother.blood_group)
    mother.nationality = data.get('nationality', mother.nationality)
    mother.email = data.get('email', mother.email)

    # If password is provided, hash and update it
    password = data.get('password')
    if password:
        mother.password = generate_password_hash(password)

    db.session.commit()
    return jsonify({"message": "Mother details updated successfully"}), 200


# Delete Mother
@mother_bp.route('/delete_mother/<string:mother_id>', methods=['DELETE'])
def delete_mother(mother_id):
    # Find the mother by ID
    mother = Mother.query.get(mother_id)
    if not mother:
        return jsonify({"error": "Mother not found"}), 404

    # Delete the mother record
    db.session.delete(mother)
    db.session.commit()
    return jsonify({"message": "Mother deleted successfully"}), 200

@mother_bp.route('/show_mothers', methods=['GET'])
def get_mothers():
    mothers = Mother.query.all()
    return jsonify(
        {
            "id": m.id,
            "first_name": m.first_name,
            "last_name": m.last_name,
            "age": m.age,
            "email": m.email,
            "blood_group": m.blood_group,
            "genotype": m.genotype,
            "nationality": m.nationality,
            "hospital_id": m.hospital_id
        } for m in mothers
    )

# Fetching a mother by ID
@mother_bp.route('/mother/<string:mother_id>', methods=['GET'])
def get_mother(mother_id):
    mother = Mother.query.get_or_404(mother_id)
    return jsonify({
        "id": mother.id,
        "full_name": f"{mother.first_name} {mother.last_name}",
        "age": mother.age,
        "email": mother.email or "",
        "blood_group": mother.blood_group,
        "genotype": mother.genotype,
        "nationality": mother.nationality,
        "hospital_id": mother.hospital_id,
        "created_at": mother.created_at.strftime('%Y-%m-%d %H:%M:%S') if mother.created_at else None,
        "updated_at": mother.updated_at.strftime('%Y-%m-%d %H:%M:%S') if mother.updated_at else None,
    })
