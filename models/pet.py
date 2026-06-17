from sqlalchemy.orm import validates
from config import db
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BaseModel

class Pet(BaseModel):
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
  
  #fields a client may change via update_db; prevents mass-assignment of
  #user_id/id/species_id from a raw request body
  updatable_fields = {'name', 'age', 'weight'}

  #methods to communicate with database
  @classmethod
  def create_row(cls, name, age, weight, species, user):
    pet = cls(name=name, age=age, weight=weight, species_id=species, user_id=user)
    pet.save_db()
    return pet