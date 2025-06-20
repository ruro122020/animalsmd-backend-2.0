from flask import request, session, jsonify
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

def add_pets_symptoms(user_pet, pet):
  """Add symptoms to the pet."""
  for symptom_name in user_pet.get('symptoms'):
    symptom = Symptom.query.filter_by(name = symptom_name).first()
    if symptom:
     PetSymptom.create_row(pet=pet, symptom=symptom)
    else:
      return {"error": f"pet '{symptom_name}' symptom  does not exist"}, 400
  return None

class Pets(Resource):
  def get(self):
    user_pets = Pet.query.filter_by(user_id = session.get('user_id')).order_by(Pet.id).all()
    return pet_schema_many.dump(user_pets), 200
    
  def post(self):
    user_pet = request.get_json()
    
    if not user_pet:
      return {"error": 'User pet info missing'}, 400
   
    pet_exist = Pet.query.filter_by(name=user_pet.get('name')).first()

    if pet_exist:
      return {"error":"Pet already Exist"}, 409

    user_id = session.get('user_id')
    species_name = user_pet.get('type')
    user = get_user(user_id)
    species = get_species(species_name.lower())
    
    if not user:
      return {"error":"user of pet does not exist"}, 400

    if not species:
      return {"error":"species of pet does not exist"}, 400

    pet = create_pet(user_pet, user, species)

    if not user_pet.get('symptoms'):
      return {"error":"symptoms are missing"}, 400
    #user_pet: is an object from the frontend
    #pet: is the object created in create_pet
    error_message = add_pets_symptoms(user_pet, pet)

    if error_message:
      return error_message
    return pet_schema.dump(pet), 200

api.add_resource(Pets, '/user/pets', endpoint='pets')