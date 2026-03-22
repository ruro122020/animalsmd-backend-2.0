from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models.models import Pet
from marshmallow_schemas.pet import pet_schema


class PetByID(Resource):
  def get(self, id):
    pet = Pet.query.filter_by(id=id).first()
    if not pet:
      return {"error": "Pet does not exist"}, 404
    if pet.user_id != session.get('user_id'):
      return {"error": "Unauthorized"}, 403
    return pet_schema.dump(pet), 200

  def delete(self, id):
    pet = Pet.query.filter_by(id=id).first()
    if not pet:
      return {"error": "Pet does not exist"}, 404
    if pet.user_id != session.get('user_id'):
      return {"error": "Unauthorized"}, 403
    Pet.delete_db(pet)
    return {}, 200

  def patch(self, id):
    pet = Pet.query.filter_by(id=id).first()
    if not pet:
      return {"error": "Pet does not exist"}, 404
    if pet.user_id != session.get('user_id'):
      return {"error": "Unauthorized"}, 403
    pet_from_user = request.get_json()
    pet.update_db(pet_from_user)
    return pet_schema.dump(pet), 200

api.add_resource(PetByID, '/user/pets/<int:id>', endpoint='user_pet_id')