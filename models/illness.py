from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

class Illness(db.Model):
  __tablename__ = 'illnesses'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  description = db.Column(db.String, nullable=False)
  remedy = db.Column(db.String)

  #relationship with illnesses table
  illness_symptom = db.relationship('IllnessSymptom', back_populates='illness', cascade="all, delete-orphan")
  
  #relationship with illnessclassification
  illness_classification = db.relationship('IllnessClassification', back_populates='illness', cascade='all, delete-orphan')
  
  #relationship with illnessmedication
  illness_medication = db.relationship('IllnessMedication', back_populates = 'illness', cascade='all, delete-orphan' )

  #relationship with illnessproduct
  illness_product = db.relationship('IllnessProduct', back_populates='illness', cascade='all, delete-orphan' )

  @hybrid_property
  def products(self):
    return [illness.product for illness in self.illness_product]
  
  @hybrid_property
  def symptoms(self):
    return [illness.symptom for illness in self.illness_symptom]
  
  @hybrid_property
  def medications(self):
    return [illness.medication for illness in self.illness_medication]
  
  @classmethod
  def create_row(cls, name, description, remedy):
    illness = cls(name=name, description=description, remedy=remedy )
    illness.save_db()
    return illness
  
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