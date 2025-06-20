from config import db, app
from models.models import Classification
from .classifications_data import classifications_data



with app.app_context():
  for element in classifications_data:
    Classification.create_row(element)

