from app import db
import uuid
#from app.models.mother_model import Mother
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class Hospital(db.Model):
	__tablename__ = "hospitals"

	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	hospital_name = db.Column(db.String(100), nullable=False)
	hospital_address = db.Column(db.String(100), nullable=False)
	phone_number = db.Column(db.Integer, nullable=False)
	email = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(150), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	# Relationship
	mothers = db.relationship('Mother', backref='hospital', lazy=True)
 
 
def set_password(self, password):
        self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)

def __repr__(self):
    return f"<Hospital id={self.id}, name={self.name}, email={self.email}>"