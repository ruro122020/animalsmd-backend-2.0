from config import app, db
from models.models import Symptom
from .symptoms_data import symptoms_data



def seed_symptoms():
  with app.app_context():
    for symptom in symptoms_data:
      #first check if symptom already exist in database
      symptom_db = Symptom.query.filter_by(name=symptom).first()
      if not symptom_db:
        Symptom.create_row(symptom)



seed_symptoms()