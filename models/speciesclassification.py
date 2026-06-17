from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BaseModel

class SpeciesClassification(BaseModel):
  __tablename__ = 'speciesclassifications'

  id = db.Column(db.Integer, primary_key=True)
  classification_id = db.Column(db.Integer, db.ForeignKey('classifications.id'))
  species_id = db.Column(db.Integer, db.ForeignKey('species.id'))

  
  #relationships
  classification = db.relationship('Classification', back_populates='species_classification')
  species = db.relationship('Species', back_populates='species_classification')


  @validates('classification_id')
  def validate_classification(self, key, classification_id):
    if classification_id is None:
      raise ValueError('classification must not be None')
    return classification_id
  
  @validates('species_id')
  def validate_species(self, key, species_id):
    if species_id is None:
      raise ValueError('species_id must not be None')
    return species_id
  
#hybrid_property is being used for the getter and setter 
#because classification and species attributes are NOT columns
#in the database and @validates, validates columns not instances
  @hybrid_property
  def classification_obj(self):
    return self._classification
    
  @classification_obj.setter
  def classification_obj(self, value):
    from models.models import Classification
    if not isinstance(value, Classification):
      raise ValueError('classification must be an instance of Classification')
    else:
     self._classification = value

  @hybrid_property
  def species_obj(self):
    return self._species
  
  @species_obj.setter
  def species_obj(self, value):
    from models.models import Species
    if not isinstance(value, Species):
      raise ValueError('species must be an instance of Species')
    else:
      self._species = value
    
  @classmethod
  def create(cls, species, classification):
    species_classification = cls(classification=classification, species=species)
    species_classification.save_db()
    return species_classification

