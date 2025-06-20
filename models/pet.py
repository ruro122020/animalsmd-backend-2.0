from sqlalchemy.orm import validates
from config import db
from sqlalchemy.ext.hybrid import hybrid_property

class Pet(db.Model):
  __tablename__ = 'pets'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer, nullable=False)
  weight = db.Column(db.Integer, nullable=False)
  species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  #relationships
  pet_symptoms = db.relationship('PetSymptom', back_populates='pet')

  #validations

  #method to get list of pet symptoms
  @hybrid_property
  def symptoms(self):
    return [pet.symptom for pet in self.pet_symptoms]
  
  #methods to communicate with database
  @classmethod
  def create_row(cls, name, age, weight, species, user):
    pet = cls(name=name, age=age, weight=weight, species_id=species, user_id=user)
    pet.save_db()
    return pet
  
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