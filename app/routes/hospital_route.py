from flask import Blueprint, request, jsonify
from app import db
from app.models.hospital_model import Hospital
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, get_jwt_identity
)

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
    access_token = create_access_token(identity=hospital.id)
    refresh_token = create_refresh_token(identity=hospital.id)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200
    
    
    
    # Refresh Token Endpoint
@hospital_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # Get the identity of the currently logged-in user
    current_hospital_id = get_jwt_identity()
    
    # Generate a new access token
    new_access_token = create_access_token(identity=current_hospital_id)
    
    return jsonify({
        "message": "Access token refreshed successfully",
        "access_token": new_access_token
    }), 200

@hospital_bp.route('/protected', methods=['GET'])
@jwt_required()  # Requires a valid access token
def protected():
    return jsonify({"message": "This is a protected route"}), 200

# Fetching all hospitals
@hospital_bp.route('/show_hospitals', methods=['GET'])
def get_hospitals():
    hospitals = Hospital.query.all()
    return jsonify(
        [
            {
                "id": h.id,
                "hospital_name": h.hospital_name,
                "hospital_address": h.hospital_address,
                "phone_number": h.phone_number,
                "email": h.email,
                "created_at": h.created_at,
            } for h in hospitals
        ]
    )

# Fetching a hospital by ID
@hospital_bp.route('/hospital/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    return jsonify({
        "id": hospital.id,
        "hospital_name": hospital.hospital_name,
        "hospital_address": hospital.hospital_address,
        "phone_number": hospital.phone_number,
        "email": hospital.email,
        "created_at": hospital.created_at,
        "updated_at": hospital.updated_at
    })