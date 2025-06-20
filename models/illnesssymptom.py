from sqlalchemy import Nullable
from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property


class IllnessSymptom(db.Model):
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
  
  def save_db(self):
    db.session.add(self)
    db.session.commit()

  def update_db(self, new_values):
    for key, value in new_values.items():
      setattr(self, key, value)
    db.session.commit()

  def delete_db(self):
    db.session.delete(self)
    db.session.commit()

