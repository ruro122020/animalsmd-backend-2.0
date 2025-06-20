from config import ma
from models.models import PetSymptom
from flask_marshmallow.fields import fields


class PetSymptomSchema(ma.Schema):
  class Meta:
    model = PetSymptom
    load_instance = True
    

  id = ma.Integer()
  pet_id = ma.Integer()
  symptom_id = ma.Integer()
  pet = fields.Nested('PetSchema')
  symptom = fields.Nested('SymptomSchema')


pet_symptom_schema = PetSymptomSchema()
pet_symptom_schema_many = PetSymptomSchema(many=True)