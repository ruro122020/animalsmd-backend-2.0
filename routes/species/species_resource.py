from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models.models import Species
from marshmallow_schemas.species import species_schema_many

#SpeciesResource was used to avoid name conflict with Species model
class SpeciesResource(Resource):
  def get(self):
    species = Species.query.all()
    return species_schema_many.dump(species)


api.add_resource(SpeciesResource, '/species', endpoint='species')