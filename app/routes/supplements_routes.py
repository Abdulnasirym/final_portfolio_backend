from app import db
from uuid import UUID
from flask import abort
from app.models.supplements import Supplement
from flask import Blueprint, request, jsonify, abort

supplements = Blueprint('supplements', __name__)

# Adding suplement
@supplements.route('/add_supplements', methods=['POST', 'GET'])
def add_supplement():
	data = request.json
	new_supplement = Supplement(name=data['name'], description=data.get('description'))
	db.session.add(new_supplement)
	db.session.commit()
	return jsonify({'message': 'Supplement added successfully', 'id': str(new_supplement.id)}), 201

# Getting all supplements
@supplements.route('/show_supplements', methods=['GET', 'POST'])
def get_supplements():
	supplements = Supplement.query.all()
	return jsonify([{'id': str(s.id), 'name': s.name, 'description': s.description} for s in supplements])

# Getting a supplement based on id
@supplements.route('/supplement/<string:supplement_id>', methods=['GET'])
def get_supplement(supplement_id):
	supplement = Supplement.query.get_or_404(supplement_id)

	return jsonify({
		"id": str(supplement.id),
		"name": supplement.name,
		"description": supplement.description,
		"created_at": supplement.created_at,
		"updated_at": supplement.updated_at
	})

# Updating supplements
@supplements.route('/update_supplements/<string:supplement_id>', methods=['PUT'])
def update_supplement(supplement_id):
	data = request.json
	supplement = Supplement.query.get_or_404(supplement_id)
	supplement.name = data.get('name', supplement.name)
	supplement.description = data.get('description', supplement.description)
	db.session.commit()
	return jsonify({'message': 'Supplement updated successfully'})

# Deleting supplements
@supplements.route('/delete_supplements/<string:supplement_id>', methods=['DELETE'])
def delete_supplement(supplement_id):
	supplement = Supplement.query.get_or_404(supplement_id)
	db.session.delete(supplement)
	db.session.commit()
	return jsonify({'message': 'Supplement deleted successfully'})