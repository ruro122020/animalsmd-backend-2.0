from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BaseModel


class IllnessClassification(BaseModel):
  __tablename__ = 'illnessesclassifications'

  id = db.Column(db.Integer, primary_key=True)
  illness_id = db.Column(db.Integer, db.ForeignKey('illnesses.id'), nullable=False)
  classification_id = db.Column(db.Integer, db.ForeignKey('classifications.id'), nullable=False)

  illness = db.relationship('Illness', back_populates='illness_classification')
  classification = db.relationship('Classification', back_populates='illness_classification')

  @classmethod
  def create_row(cls, illness, classification):
    illness_classification = cls(illness=illness, classification=classification)
    illness_classification.save_db()
    return illness_classification