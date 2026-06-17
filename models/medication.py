from config import db
from .base import BaseModel

class Medication(BaseModel):
  __tablename__ = 'medications'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  description = db.Column(db.String, nullable=False)

  #relationships
  #relationship with illnessmedication
  illness_medication = db.relationship('IllnessMedication', back_populates = 'medication', cascade='all, delete-orphan')

  #fields a client may change via update_db
  updatable_fields = {'name', 'description'}

  @classmethod
  def create_row(cls, name, description):
    pet = cls(name=name, description=description)
    pet.save_db()
    return pet