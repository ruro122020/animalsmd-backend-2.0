from config import db

class Medication(db.Model):
  __tablename__ = 'medications'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  description = db.Column(db.String, nullable=False)

  #relationships
  #relationship with illnessmedication
  illness_medication = db.relationship('IllnessMedication', back_populates = 'medication', cascade='all, delete-orphan')
  
  @classmethod
  def create_row(cls, name, description):
    pet = cls(name=name, description=description)
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