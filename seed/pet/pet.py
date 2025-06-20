from config import app
from models.models import Pet, Species, User
from .pets_data import pet_data



with app.app_context():
  for pet in pet_data:
    species = Species.query.filter_by(id=pet.get('species_id')).first()
    user = User.query.filter_by(id=pet.get('user_id')).first()
    Pet.create_row(pet.get('name'), pet.get('age'),pet.get('weight'), species.id, user.id)  
  
