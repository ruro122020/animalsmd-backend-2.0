from flask import request, session
from flask_restful import Resource
from config import api, db
from models.models import Product, IllnessSymptom, Illness, IllnessClassification, SpeciesClassification, Pet
from sqlalchemy import func
from marshmallow_schemas.illness import illness_schema 
from marshmallow_schemas.illnesssymptom import illness_symptom_schema
from marshmallow_schemas.pet import pet_schema
from marshmallow_schemas.product import product_schema

#The end goal is to return illness, medications, and products from results

def create_illnesses_ids_list(symptoms_list):
  #When query illness_symptoms, the same illness is returned for multiple symptoms
  #to avoid duplicate ids, we are using the set data structure
  symptom_ids = [symptom.id for symptom in symptoms_list]
  if not symptom_ids:
    return []
  #one query for all symptoms instead of one per symptom (avoids N+1 queries)
  illness_symptoms = IllnessSymptom.query.filter(
    IllnessSymptom.symptom_id.in_(symptom_ids)).all()
  return list({illness_symptom.illness_id for illness_symptom in illness_symptoms})

def create_illness_list(classification_illness, illness_ids):
  #compare the returned list from IllnessesClassifications table to the illness_list
  matched_ids = {
    ic.illness_id for ic in classification_illness if ic.illness_id in illness_ids
  }
  if not matched_ids:
    return []
  #one query for all matched illnesses instead of one per illness (avoids N+1)
  return Illness.query.filter(Illness.id.in_(matched_ids)).all()

def get_pets_classification_id(pet):
  #query the speciesclassifications table to find the classification id of the species 
  species_classification = SpeciesClassification.query.filter_by(species_id = pet.species_id).first()
  return species_classification.classification

def get_illnesses_based_on_pets_classification(pet_classification):
  #use classification's id to query the illnessclassifications table, return all illness that matched the classification_id
  return IllnessClassification.query.filter_by(classification_id = pet_classification.id).all()

class PetResults(Resource):
  def get(self, id):
    #get user's pet from database
    pet = Pet.query.filter_by(id=id).first()

    if not pet:
      return {"error": "pet id not found or pet does not exist"}, 400
    if pet.user_id != session.get('user_id'):
      return {"error": "Unauthorized"}, 403
    #Now we want to get all the illnesses that matches the symptoms id
    illness_ids = create_illnesses_ids_list(pet.symptoms)

    #Now we want to make sure that the illnesses belongs to the classification of the pet
    #for instance, if a user's pet is a dog and the dogs classification is a mammal, 
    #we don't want to return illnesses that belong to a reptile classification
    
    #get the pet's classification id
    pet_classification = get_pets_classification_id(pet)
    
    illnesses_based_on_pets_classification = get_illnesses_based_on_pets_classification(pet_classification)

    #this illness_list needs to be serialized 
    illness_list = create_illness_list(illnesses_based_on_pets_classification, illness_ids)
      
    #Now we have to serialize each illness in the illness_list
    serialized_illness_list = [illness_schema.dump(illness) for illness in illness_list]
    
    if not serialized_illness_list:
      return {"error":"No Results found"}, 404
    
    return serialized_illness_list, 200


api.add_resource(PetResults, '/user/pets/<int:id>/results', endpoint='user_pet_results')