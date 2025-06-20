from config import db, app
from models.models import Pet, PetSymptom, Symptom
from .pets_symptoms_data import pet_symptoms_data

with app.app_context():
  for pet_symptom in pet_symptoms_data:
    pet = Pet.query.filter_by(id=pet_symptom.get('pet_id')).first()
    symptom = Symptom.query.filter_by(id=pet_symptom.get('symptom_id')).first()
    PetSymptom.create_row(pet, symptom)


