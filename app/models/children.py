from app import db
from datetime import datetime
import uuid

class Children(db.Model):
    __tablename__ = "children"

    children_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    parent_id = db.Column(db.String, db.ForeignKey("mothers.id"), nullable=True)
    blood_group = db.Column(db.String(20), nullable=False)
    genotype = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    parent_email = db.Column(db.String(200), nullable=False)
    nationality = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Immunization, avoiding overlaps warning
    immunizations = db.relationship(
        "Immunization",
        back_populates="child",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Children id={self.children_id}, first_name={self.first_name}, last_name={self.last_name}>"
