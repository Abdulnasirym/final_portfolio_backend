from flask import Blueprint, jsonify, request
from app import db
from app.models.mother_model import Mother
from app.models.antenatal_model import AntenatalRecord  # Assuming the model is defined here
import uuid
from datetime import datetime

antenatal_bp = Blueprint('antenatal_bp', __name__)

# Create Antenatal Record
@antenatal_bp.route('/create_antenatal_record', methods=['GET', 'POST'])
def create_antenatal_record():
    data = request.get_json()

    # Extract fields from request
    mother_id = data.get('mother_id')
    weight = data.get('weight')
    blood_pressure = data.get('blood_pressure')
    tests = data.get('tests')
    remark = data.get('remark')

    # Validate required fields
    if not all([mother_id, weight, blood_pressure]):
        return jsonify({"error": "mother_id, weight, and blood_pressure are required"}), 400

    # Check if the mother exists
    mother = Mother.query.get(mother_id)
    if not mother:
        return jsonify({"error": "Mother not found"}), 404

    # Create and save the antenatal record
    antenatal_record = AntenatalRecord(
        mother_id=mother_id,
        weight=weight,
        blood_pressure=blood_pressure,
        tests=tests,
        remark=remark
    )

    db.session.add(antenatal_record)
    db.session.commit()

    return jsonify({"message": "Antenatal record created successfully", "record": antenatal_record.id}), 201

# Retrieve Antenatal Records by Mother ID
@antenatal_bp.route('/get_antenatal_record/<string:mother_id>', methods=['GET'])
def get_antenatal_records(mother_id):
    # Check if the mother exists
    mother = Mother.query.get(mother_id)
    if not mother:
        return jsonify({"error": "Mother not found"}), 404

    # Fetch antenatal records for the mother
    records = AntenatalRecord.query.filter_by(mother_id=mother_id).all()

    records_list = [
        {
            "id": record.id,
            "weight": record.weight,
            "blood_pressure": record.blood_pressure,
            "tests": record.tests,
            "remark": record.remark,
            "date_created": record.date_created
        }
        for record in records
    ]

    return jsonify({"records": records_list}), 200

# Update Antenatal Record
@antenatal_bp.route('/update_antenatal_record/<string:record_id>', methods=['PUT'])
def update_antenatal_record(record_id):
    data = request.get_json()

    # Find the antenatal record by ID
    record = AntenatalRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Antenatal record not found"}), 404

    # Update fields if provided
    record.weight = data.get('weight', record.weight)
    record.blood_pressure = data.get('blood_pressure', record.blood_pressure)
    record.tests = data.get('tests', record.tests)
    record.remark = data.get('remark', record.remark)

    # Commit the changes to the database
    db.session.commit()
    return jsonify({"message": "Antenatal record updated successfully"}), 200

# Delete Antenatal Record
@antenatal_bp.route('/delete_antenatal_record/<string:record_id>', methods=['DELETE'])
def delete_antenatal_record(record_id):
    # Find the antenatal record by ID
    record = AntenatalRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Antenatal record not found"}), 404

    # Delete the record
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Antenatal record deleted successfully"}), 200

@antenatal_bp.route('/get_all_antenatal_records', methods=['GET'])
def get_all_antenatal_records():
    antenatal_records = AntenatalRecord.query.all()

    records_list = []
    for record in antenatal_records:
        # Fetch mother information for each record
        mother = Mother.query.get(record.mother_id)
        mother_full_name = f"{mother.first_name} {mother.last_name}" if mother else "Unknown Mother"

        records_list.append({
            "id": record.id,
            "mother_name": mother_full_name,
            "weight": record.weight,
            "blood_pressure": record.blood_pressure,
            "tests": record.tests or "",
            "remark": record.remark or "",
            "date_created": record.date_created.strftime('%Y-%m-%d %H:%M:%S') if record.date_created else None
        })

    return jsonify({
        "antenatal_records": records_list
    }), 200
