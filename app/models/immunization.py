from app import db
import uuid
from datetime import datetime, date

class Immunization(db.Model):

    __tablename__ = "immunization"

    immunization_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    children_id = db.Column(db.String(200), db.ForeignKey("children.children_id"), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    parent_id = db.Column(db.String, db.ForeignKey("mothers.id"), nullable=True)
    parent_first_name = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    parent_email = db.Column(db.String(200), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    injections = db.Column(db.Text, nullable=True)
    previous_date = db.Column(db.Date, nullable=False)  
    next_date = db.Column(db.Date, nullable=False)  
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)

    child = db.relationship(
        "Children",
        back_populates="immunizations",
        lazy=True
    )


    def __repr__(self):
        return f"<Children id={self.id}, first_name={self.first_name}, last_name={self.last_name}, parent_email={self.parent_email}>"
