# from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db
from sqlalchemy.ext.hybrid import hybrid_property


class Species(db.Model):
  __tablename__ = 'species'

  id = db.Column(db.Integer, primary_key=True)
  type_name = db.Column(db.String, nullable=False)

  #relationships
  species_classification = db.relationship('SpeciesClassification', back_populates='species')

  #hybrid_property is being used for the getter and setter 
  #because classification and species attributes are NOT columns
  #in the database and @validates, validates columns not instances
  @validates('type_name')
  def validates_type_name(self, key, type_name):
    if type_name is None or not type(type_name) == str:
      raise ValueError("type_name must not be None. Must be a string")
    else:
      return type_name

  @hybrid_property
  def species_classification_obj(self):
    return self._species_classification

  @species_classification_obj.setter
  def species_classification_obj(self, value):
    from models.models import SpeciesClassification
    if not isinstance(value, SpeciesClassification):
      raise ValueError('value must be an instance of SpeciesClassification')
    else:
      self._species_classification = value

  @classmethod
  def create_row(cls, type_name):
    type_name_obj = cls(type_name=type_name)
    type_name_obj.save_db()
    return type_name_obj
  
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