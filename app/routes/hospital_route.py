from flask import Blueprint, request, jsonify
from app import db
from app.models.hospital_model import Hospital
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

hospital_bp = Blueprint('hospital_bp', __name__)

# Hospital Registration
@hospital_bp.route('/register_hospital', methods=['GET', 'POST'])
def register_hospital():
    data = request.get_json()

    # Extract data from request
    name = data.get('hospital_name')
    address = data.get('hospital_address')
    phone_number = data.get('phone_number')
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not all([name, address, phone_number, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    # Check if the email already exists
    if Hospital.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists!"}), 400

    # Hash the password and save hospital information to the database
    password_hash = generate_password_hash(password)
    new_hospital = Hospital(
        hospital_name=name,
        hospital_address=address,
        phone_number=phone_number,
        email=email,
        password=password_hash
    )
    db.session.add(new_hospital)
    db.session.commit()

    return jsonify({"message": "Hospital registered successfully"}), 201

# Hospital Login
@hospital_bp.route('/login_hospital', methods=['GET','POST'])
def hospital_login():
    data = request.get_json()

    # Extract data from request
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    # Check if the email exists and verify password
    hospital = Hospital.query.filter_by(email=email).first()
    if not hospital or not check_password_hash(hospital.password, password):
        return jsonify({"error": "Invalid email or password"}), 400

    # Generate a JWT token
    token = create_access_token(identity=hospital.id)
    return jsonify({"message": "Login successful"}), 200
