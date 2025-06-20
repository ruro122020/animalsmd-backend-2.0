from config import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property


class IllnessClassification(db.Model):
  __tablename__ = 'illnessesclassifications'

  id = db.Column(db.Integer, primary_key=True)
  illness_id = db.Column(db.Integer, db.ForeignKey('illnesses.id'), nullable=False)
  classification_id = db.Column(db.Integer, db.ForeignKey('classifications.id'), nullable=False)

  illness = db.relationship('Illness', back_populates='illness_classification')
  classification = db.relationship('Classification', back_populates='illness_classification')

  @classmethod
  def create_row(cls, illness, classification):
    illness_classification = cls(illness=illness, classification=classification)
    illness_classification.save_db()
    return illness_classification
  
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