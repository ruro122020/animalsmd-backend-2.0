from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

class Symptom(db.Model):
  __tablename__ = 'symptoms'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  
  #relationship with classifications table
  symptom_classifications = db.relationship('SymptomClassification', back_populates='symptom')
  
  #relationship with pets table
  pet_symptoms = db.relationship('PetSymptom', back_populates='symptom')
  
  #relationship with illnesses table
  illness_symptom = db.relationship('IllnessSymptom', back_populates='symptom')
  
  @validates('name')
  def validates_name (self, key, name):
    if name is None or not type(name) == str:
      raise ValueError("name must not be None and must be of a string")
    return name

  @hybrid_property
  def symptom_classification_obj(self):
    return self._symptom_classification_obj
  
  @symptom_classification_obj.setter
  def symptom_classification_obj(self, value):
    from models.models import SymptomClassification
    if not isinstance(value, SymptomClassification):
      raise ValueError("value must be an instance of SymptomClassification model")
    else:
      self._symptom_classification = value

  @classmethod
  def create_row(cls, name):
    name = cls(name = name)
    name.save_db()
    return name
  
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