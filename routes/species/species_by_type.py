from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models.models import Species, SpeciesClassification, SymptomClassification, Classification
from sqlalchemy.exc import IntegrityError
from marshmallow_schemas.species import species_schema
from marshmallow_schemas.speciesclassification import species_classification_schema
from marshmallow_schemas.classification import classification_schema
from marshmallow_schemas.symptomsclassification import symptom_classification_schema_many
             
class SpeciesByType(Resource):
  def get(self, type_name):
    #query species table in the database
    species = Species.query.filter(Species.type_name == type_name.lower()).first()
    #return error if not found
    if not species:
      return {"error": "Species not found"}, 404
    
    #query speciesclassification table to find what classification species is from 
    species_classification = SpeciesClassification.query.filter_by(species_id = species.id).first()
    #return error if not found
    if not species_classification:
      return {"error": "SpeciesClassification not found"}, 404
    
    #assign the classification obj, queried through species_classification
    classification_inst = species_classification.classification

    #query symptomsclassification table using the classification_inst obj to get a list of symptoms of the classification 
    classification_symptoms = SymptomClassification.query.filter_by(classification = classification_inst).all()
    #return error if not found
    if not classification_symptoms:
      return {"error": "SymptomClassification not found"}, 404
    
    # classification_symptoms data structure is an array these: 
    # {
    #     "classification": {
    #         "id": 1,
    #         "classification": "mammal"
    #     },
    #     "symptom": {
    #         "id": 1,
    #         "name": "skin lesions"
    #     },
    #     "id": 2
    # }
    #Therefore we must iterate through and format the object how we want to send back. 
    # Data structure to return:
    # {
    #   "classification":"mammal",
    #   "symptoms": ["...array of symptoms"],
    #   "id": 1
    # }
    
    #create symptoms array
    symptoms = [ classification_symptom.symptom.name for classification_symptom in classification_symptoms ]

    response_obj = {
      "classification": classification_inst.classification,
      "symptoms": symptoms,
      "classification_id": classification_inst.id
    }
    
    return response_obj, 200

api.add_resource(SpeciesByType, '/species/<type_name>')