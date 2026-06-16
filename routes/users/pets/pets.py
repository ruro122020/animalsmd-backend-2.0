from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models.models import Pet, User, Species, PetSymptom, Symptom
from utils.authenticate import authenticate
from marshmallow_schemas.pet import pet_schema_many, pet_schema

def get_user(user_id):
  """Fetch the user by ID."""
  return User.query.filter_by(id=user_id).first()


def get_species(species_name):
  """Fetch the species by type name."""
  return Species.query.filter_by(type_name = species_name).first()
 
def create_pet(pet, user, species):
  """Create a new pet row."""
  return Pet.create_row(name = pet.get('name'), age = pet.get('age'), weight=pet.get('weight'), user=user.id, species=species.id)#id's had to be passed cause Pet model has no validations yet. 

class Pets(Resource):
  def get(self):
    user_pets = Pet.query.filter_by(user_id = session.get('user_id')).order_by(Pet.id).all()
    return pet_schema_many.dump(user_pets), 200
    
  def post(self):
    user_pet = request.get_json()
    
    if not user_pet:
      return {"error": 'User pet info missing'}, 400
   
    user_id = session.get('user_id')
    species_name = user_pet.get('type')
    if not species_name:
      return {"error": "species type is missing"}, 400

    if not user_pet.get('symptoms'):
      return {"error": "symptoms are missing"}, 400

    #name uniqueness is scoped to the account, so different users can reuse names
    pet_exist = Pet.query.filter_by(name=user_pet.get('name'), user_id=user_id).first()
    if pet_exist:
      return {"error":"Pet already Exist"}, 409

    user = get_user(user_id)
    species = get_species(species_name.lower())
    
    if not user:
      return {"error":"user of pet does not exist"}, 400

    if not species:
      return {"error":"species of pet does not exist"}, 400

    #resolve every symptom before creating the pet so a bad symptom name
    #doesn't leave an orphaned pet in the database
    symptoms = []
    for symptom_name in user_pet.get('symptoms'):
      symptom = Symptom.query.filter_by(name=symptom_name).first()
      if not symptom:
        return {"error": f"pet '{symptom_name}' symptom  does not exist"}, 400
      symptoms.append(symptom)

    pet = create_pet(user_pet, user, species)
    for symptom in symptoms:
      PetSymptom.create_row(pet=pet, symptom=symptom)

    return pet_schema.dump(pet), 200

api.add_resource(Pets, '/user/pets', endpoint='pets')