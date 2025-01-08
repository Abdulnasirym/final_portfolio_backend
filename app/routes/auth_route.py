from flask import request, jsonify, Blueprint
from app.models.mother_model import Mother
from app.utils.auth import hash_password, verify_password, generate_token  # Ensure correct import paths
from app import db

# Blueprint object for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

# User Registration
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Extract data from request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    hospital_id = data.get('hospital_id')

    # Validate required fields
    if not all([first_name, last_name, email, phone_number, password, hospital_id]):
        return jsonify({"message": "All fields are required"}), 400

    # Check if the email is already taken
    if Mother.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    # Hash the password and create a new mother record
    hashed_password = hash_password(password)
    new_mother = Mother(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password_hash=hashed_password,
        hospital_id=hospital_id
    )

    db.session.add(new_mother)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": new_mother.id}), 201

# User Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Extract data from request
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Find the user by email
    mother = Mother.query.filter_by(email=email).first()

    # Validate user and password
    if not mother or not verify_password(mother.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate token
    token = generate_token(mother.id)

    return jsonify({"message": "Login successful", "token": token}), 200
