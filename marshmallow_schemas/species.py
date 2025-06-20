from config import ma
from models.models import Species
from flask_marshmallow.fields import fields

class SpeciesSchema(ma.Schema):
  class Meta:
    model = Species
    load_instance = True
    fields = ('id','type_name', 'species_classification')
  
  species_classification = fields.Nested("SpeciesClassificationSchema")



species_schema = SpeciesSchema()
species_schema_many = SpeciesSchema(many=True)