from config import ma
from models.models import Pet
from flask_marshmallow.fields import fields

class PetSchema(ma.Schema):
  class Meta:
    model = Pet
    load_instance = True
    fields = ('id', 'name', 'age', 'weight', 'user_id', 'species_id', 'symptoms')

  symptoms = fields.List(fields.Nested("SymptomSchema"))

pet_schema = PetSchema()
pet_schema_many = PetSchema(many=True)