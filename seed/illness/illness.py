from config import db, app
from models.models import Illness
from .illnesses_data import illnesses_data

#helpers

def has_illness(illness):
  illness_db = Illness.query.filter_by(name=illness).first()
  return illness_db

#############

def seed_illness_table():
  with app.app_context():
    for illness, description_remedy_obj in illnesses_data.items():
      description = description_remedy_obj.get('description')
      remedy = description_remedy_obj.get('remedy')
    
      if not has_illness(illness):
        Illness.create_row(name=illness, description=description, remedy=remedy)

seed_illness_table()