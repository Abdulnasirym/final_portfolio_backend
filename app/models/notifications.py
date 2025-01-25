from app import db
from datetime import datetime
import uuid

class Notification(db.Model):
	__tablename__ = 'notifications'

	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	user_id = db.Column(db.Integer, nullable=False)
	message = db.Column(db.Text, nullable=False)
	is_read = db.Column(db.Boolean, default=False, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	send_at = db.Column(db.DateTime, nullable=True)