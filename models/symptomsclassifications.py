from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

class SymptomClassification(db.Model):
  __tablename__ = 'symptomsclassifications'

  id = db.Column(db.Integer, primary_key=True)
  classification_id = db.Column(db.Integer, db.ForeignKey('classifications.id'))
  symptoms_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'))

  #relationships
  classification = db.relationship('Classification', back_populates='symptom_classifications')
  symptom = db.relationship('Symptom', back_populates='symptom_classifications')
  
  @validates("classification_id")
  def validates_classification(self,key, classification_id):
    if classification_id is None:
      raise ValueError('classification must not be None')
    return classification_id
  
  @validates('symptom_id')
  def validate_symptom(self, key, symptom_id):
    if symptom_id is None:
      raise ValueError('symptom_id must not be None')
    return symptom_id
  
  @hybrid_property
  def classification_obj(self):
    return self._classification 
  
  @classification_obj.setter
  def classification_obj(self, value):
    from models.models import Classification
    if not isinstance(value, Classification):
      raise ValueError('value must be an instance of Classification')
    else:
      self._classification = value

  @hybrid_property
  def symptom_obj(self):
    return self._symptom
  
  @symptom_obj.setter
  def symptom_obj(self, value):
    from models.models import Symptom
    if not isinstance(value, Symptom):
      raise ValueError("value must be an instance of Symptom")
    else:
      self._symptom = value

  @classmethod
  def create_row(cls, classification_inst, symptom_inst):
    symptomclassification = cls(classification = classification_inst, symptom= symptom_inst)
    symptomclassification.save()
    return symptomclassification
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def update_db(self, new_values):
    for key, value in new_values.items():
      setattr(self, key, value)
    db.session.commit()

  def delete_db(self):
    db.session.delete(self)
    db.session.commit()