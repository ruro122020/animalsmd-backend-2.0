from sqlalchemy.orm import validates
from config import db
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BaseModel


class Classification(BaseModel):
  __tablename__ = 'classifications'

  id = db.Column(db.Integer, primary_key=True)
  classification = db.Column(db.String, nullable=False)

  #fields a client may change via update_db
  updatable_fields = {'classification'}

  #relationships
  
  #relationship between species and classification. This line points to SpeciesClassification association table
  species_classification = db.relationship('SpeciesClassification', back_populates='classification')
  
  #relationship between symptoms and classification. This line points to SymptomClassification association table
  symptom_classifications = db.relationship('SymptomClassification', back_populates='classification')
  
  #relationship between illness and classification. 
  illness_classification = db.relationship('IllnessClassification', back_populates='classification', cascade='all, delete-orphan')
  
  #hybrid_property is being used for the getter and setter 
  #because classification and species attributes are NOT columns
  #in the database and @validates, validates columns not instances
  @validates('classification')
  def validates_classification(self, key, classification):
    if classification is None or not type(classification) == str:
      raise ValueError('classification must not be None. Must be of type string.')
    return classification
  
  @hybrid_property
  def species_classification_obj(self):
    return self._species_classification 
  
  @species_classification_obj.setter
  def species_classification_obj(self, value):
    from models.models import SpeciesClassification
    if not isinstance(value, SpeciesClassification):
      raise ValueError('classification must be an instance of Classification')
    else:
      self._species_classification = value

    
  @classmethod
  def create_row(cls, classification):
    classification = cls(classification=classification)
    classification.save_db()
    return classification
