from app import db
from datetime import datetime
import uuid

class Supplement(db.Model):
    __tablename__ = 'supplements'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mother_id = db.Column(db.String(36), db.ForeignKey('mothers.id'), nullable=False)  # Foreign key reference to Mother
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationship to Mother
    mother = db.relationship('Mother', back_populates='supplements', lazy=True)

    def __repr__(self):
        return f"<Supplement name={self.name}>"


