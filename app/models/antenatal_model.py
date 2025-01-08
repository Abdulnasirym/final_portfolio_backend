from app import db
import uuid
from datetime import datetime
from app.models.mother_model import Mother

class AntenatalRecord(db.Model):  # Corrected the name to AntenatalRecord
    __tablename__ = "antenatal_records"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID for better uniqueness
    weight = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.String(20), nullable=False)
    tests = db.Column(db.Text, nullable=True)
    remark = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign key referencing Mother table
    mother_id = db.Column(
        db.String(36),  # Consistent UUID format
        db.ForeignKey('mothers.id'), 
        nullable=False
    )

    # Relationship with Mother
    mother = db.relationship('Mother', backref='antenatal_records', lazy=True)

    def __repr__(self):
        return (
            f"<AntenatalRecord id={self.id}, mother_id={self.mother_id}, "
            f"weight={self.weight}, blood_pressure={self.blood_pressure}, date_created={self.date_created}>"
        )
