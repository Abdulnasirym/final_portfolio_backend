from flask import request, Blueprint, jsonify
from app.models.antenatal_model import AntenatalRecord  # Corrected the model import to AntenatalRecord
from app.models.mother_model import Mother
from app import db
from app.utils.auth import decode_token  # Ensure the correct path for imports

# Blueprint for antenatal-related routes
antenatal_bp = Blueprint('antenatal_bp', __name__)

# Helper function for user authentication
def authenticate_user():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return None, "Authorization token not found", 401

    token = auth_header.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return None, "Invalid token", 401

    user = Mother.query.get(user_id)
    if not user:
        return None, "User not found", 401

    return user, None, 200

# Endpoint to register a new antenatal visit
@antenatal_bp.route('/register_antenatal_visit', methods=['POST'])
def create_antenatal():
    user, message, status_code = authenticate_user()
    if not user:
        return jsonify({"message": message}), status_code

    data = request.get_json()

    weight = data.get('weight')
    blood_pressure = data.get('blood_pressure')
    tests = data.get('tests')
    date = data.get('date')  # Ensure valid date format is passed
    remark = data.get('remark')

    # Validate required fields
    if not weight:
        return jsonify({"error": "Weight is required!"}), 400
    if not blood_pressure:
        return jsonify({"error": "Blood pressure is required!"}), 400
    if not date:
        return jsonify({"error": "Date is required!"}), 400

    # Create and save a new antenatal record
    new_record = AntenatalRecord(  # Use AntenatalRecord instead of Antenatal
        mother_id=user.id,
        date=date,
        weight=weight,
        blood_pressure=blood_pressure,
        tests=tests,
        remark=remark
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "Antenatal record created successfully!"}), 201

# Endpoint to retrieve all antenatal records for the authenticated user
@antenatal_bp.route('/antenatal_records', methods=['GET'])
def get_all_antenatal_records():
    user, message, status_code = authenticate_user()
    if not user:
        return jsonify({"message": message}), status_code

    records = AntenatalRecord.query.filter_by(mother_id=user.id).all()  # Corrected to AntenatalRecord
    response = [
        {
            "id": record.id,
            "date": record.date.strftime('%Y-%m-%d'),
            "weight": record.weight,
            "blood_pressure": record.blood_pressure,
            "tests": record.tests,
            "remark": record.remark,
        }
        for record in records
    ]

    return jsonify(response), 200

# Endpoint to retrieve a specific antenatal record
@antenatal_bp.route('/antenatal_record/<string:id>', methods=['GET'])
def get_antenatal_record(id):
    user, message, status_code = authenticate_user()
    if not user:
        return jsonify({"message": message}), status_code

    record = AntenatalRecord.query.get(id)  # Corrected to AntenatalRecord
    if not record:
        return jsonify({"error": "Record not found!"}), 404

    if record.mother_id != user.id:
        return jsonify({"message": "Unauthorized"}), 403

    response = {
        "id": record.id,
        "date": record.date.strftime('%Y-%m-%d'),
        "weight": record.weight,
        "blood_pressure": record.blood_pressure,
        "tests": record.tests,
        "remark": record.remark,
    }

    return jsonify(response), 200

# Endpoint to update an existing antenatal record
@antenatal_bp.route('/update_antenatal/<string:id>', methods=['PUT'])
def update_antenatal_record(id):
    user, message, status_code = authenticate_user()
    if not user:
        return jsonify({"message": message}), status_code

    record = AntenatalRecord.query.get(id)  # Corrected to AntenatalRecord
    if not record:
        return jsonify({"error": "Record not found!"}), 404

    if record.mother_id != user.id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    record.date = data.get('date', record.date)
    record.weight = data.get('weight', record.weight)
    record.blood_pressure = data.get('blood_pressure', record.blood_pressure)
    record.tests = data.get('tests', record.tests)
    record.remark = data.get('remark', record.remark)

    db.session.commit()
    return jsonify({"message": "Antenatal record updated successfully!"}), 200

# Endpoint to delete an antenatal record
@antenatal_bp.route('/delete_antenatal/<string:id>', methods=['DELETE'])
def delete_antenatal_record(id):
    user, message, status_code = authenticate_user()
    if not user:
        return jsonify({"message": message}), status_code

    record = AntenatalRecord.query.get(id)  # Corrected to AntenatalRecord
    if not record:
        return jsonify({"error": "Record not found!"}), 404

    if record.mother_id != user.id:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Antenatal record deleted successfully!"}), 200
