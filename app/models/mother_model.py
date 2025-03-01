from app import db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.models.antenatal_model import AntenatalRecord
from app.models.supplements import Supplement
from app.models.notifications import Notification
from app.models.hospital_model import Hospital

class Mother(db.Model):
	__tablename__ = "mothers"
	
	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	hospital_id = db.Column(db.String(36), db.ForeignKey('hospitals.id'), nullable=False)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	age = db.Column(db.Integer, nullable=False)
	genotype = db.Column(db.String(10), nullable=False)
	blood_group = db.Column(db.String(10), nullable=False)
	nationality = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	password_hash = db.Column(db.String(150), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	# RelationshipS
	supplements =db.relationship('Supplement', back_populates='mother', lazy=True)
	notifications = db.relationship('Notification', back_populates='mother', lazy=True)
	# antenatal_records = db.relationship('AntenatalRecord', backref='mother', lazy=True)
 
    # Relationship with Hospital
	hospital = db.relationship('Hospital', back_populates='mothers', lazy=True)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f"<name={self.first_name} {self.last_name}>"


