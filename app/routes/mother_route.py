from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.mother_model import Mother
from app import db
from flask_jwt_extended import create_access_token

mother_bp = Blueprint('mother_bp', __name__)

# Mother Registration
@mother_bp.route('/register_mother', methods=['POST'])
def register_mother():
    data = request.get_json()

    # Extract data from request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    blood_group = data.get('blood_group')
    genotype = data.get('genotype')
    nationality = data.get('nationality')
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if any(not field for field in [first_name, last_name, age, blood_group, genotype, nationality, email, password]):
        return jsonify({"error": "All fields are required!"}), 400

    # Check if the email already exists
    if Mother.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists!"}), 400

    # Hash the password and create new mother record
    password_hash = generate_password_hash(password)
    new_mother = Mother(
        first_name=first_name,
        last_name=last_name,
        age=age,
        blood_group=blood_group,
        genotype=genotype,
        nationality=nationality,
        email=email,
        password=password_hash
    )

    db.session.add(new_mother)
    db.session.commit()

    return jsonify({"message": "Mother registered successfully!"}), 201

# Mother Login
@mother_bp.route('/login_mother', methods=['POST'])
def mother_login():
    data = request.get_json()

    # Extract data from request
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    # Check if the mother exists and validate password
    mother = Mother.query.filter_by(email=email).first()
    if not mother or not check_password_hash(mother.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 400

    # Generate JWT token
    token = create_access_token(identity=mother.id)
    return jsonify({"message": "Login successful", "token": token}), 200
