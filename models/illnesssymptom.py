from sqlalchemy import Nullable
from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BaseModel


class IllnessSymptom(BaseModel):
  __tablename__ = 'illnessessymptoms'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  illness_id = db.Column(db.Integer, db.ForeignKey('illnesses.id'), nullable=False)
  symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)

  #relationships
  illness = db.relationship('Illness', back_populates='illness_symptom')
  symptom = db.relationship('Symptom', back_populates='illness_symptom')

  @classmethod
  def create_row(cls, illness, symptom):
    illness_symptom = cls(illness=illness, symptom=symptom)
    illness_symptom.save_db()
    return illness_symptom

