from config import db, app
from models.models import Species
from .species_data import species_data

with app.app_context():
  #create species
  for type_name in species_data:
    Species.create_row(type_name)
