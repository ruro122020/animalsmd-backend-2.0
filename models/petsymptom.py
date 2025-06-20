from sqlalchemy.orm import validates
from config import db
from sqlalchemy.ext.hybrid import hybrid_property


class PetSymptom(db.Model):
  __tablename__ = 'petsymptoms'

  id = db.Column(db.Integer, primary_key=True)
  pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
  symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'))

  #relationships
  pet = db.relationship('Pet', back_populates='pet_symptoms')
  symptom = db.relationship('Symptom', back_populates='pet_symptoms')
  
  #validations
  
  #methods
  @classmethod
  def create_row(cls, pet, symptom):
    pet_symptom = cls(pet=pet, symptom=symptom)
    pet_symptom.save_db()
    return pet_symptom
  
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