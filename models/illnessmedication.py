from sqlalchemy import ForeignKey
from config import db
from .base import BaseModel

class IllnessMedication(BaseModel):
  __tablename__ = 'illnessesmedications'

  id = db.Column(db.Integer, primary_key=True)
  illness_id = db.Column(db.Integer, ForeignKey('illnesses.id'), nullable=False)
  medication_id = db.Column(db.Integer, ForeignKey('medications.id'), nullable=False)

  #relationships
  illness = db.relationship('Illness', back_populates='illness_medication')
  medication = db.relationship('Medication', back_populates='illness_medication')

  @classmethod
  def create_row(cls, illness, medication):
    illness_symptom = cls(illness=illness, medication=medication)
    illness_symptom.save_db()
    return illness_symptom
