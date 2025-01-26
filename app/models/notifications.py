from app import db
from datetime import datetime
import uuid

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mother_id = db.Column(db.String(36), db.ForeignKey('mothers.id'), nullable=False)  # Foreign Key to Mother
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    send_at = db.Column(db.DateTime, nullable=True)

    # Relationship to Mother
    mother = db.relationship('Mother', back_populates='notifications', lazy=True)

    def __repr__(self):
        return f"<Notification message={self.message}>"
