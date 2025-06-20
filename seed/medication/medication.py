from .medications_data import medications_data
from config import app
from models.models import Medication

def seed_medications_table():
  with app.app_context():
  
    for medication, description in medications_data.items():
      #check if medication exist in medications table
      medication_exist = Medication.query.filter_by(name = medication).first()
      if not medication_exist:
       Medication.create_row(medication, description)
      

seed_medications_table()