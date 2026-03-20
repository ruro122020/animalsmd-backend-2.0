from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models.models import Pet
from marshmallow_schemas.pet import pet_schema


class PetByID(Resource):
  def get(self, id):
    pet = Pet.query.filter_by(id=id).first()
    if pet:
      return pet_schema.dump(pet), 200
    return {"error": "Pet does not exist"}, 404
  
  def delete(self, id):
    pet = Pet.query.filter_by(id=id).first()
    if pet:
      Pet.delete_db(pet)
      return {}, 200

    return {"error": "Pet does not exist"}, 404
  
  def patch(self, id):
    pet = Pet.query.filter_by(id=id).first()
    pet_from_user = request.get_json()
    if pet:
      pet.update_db(pet_from_user)
      return pet_schema.dump(pet), 200
      
    return {"error": "Pet does not exist"}, 400

api.add_resource(PetByID, '/user/pets/<int:id>', endpoint='user_pet_id')