from sqlalchemy import ForeignKey
from config import db

class IllnessMedication(db.Model):
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
