from config import ma
from models.models import Illness
from flask_marshmallow.fields import fields

class IllnessSchema(ma.Schema):
  class Meta:
    model = Illness
    load_instance = True
    include_relationships = True
    #iMPORTANT NOTICE: DON'T FORGET TO ADD THE METHODS TO THE FIELDS TUPLE!
    fields = ('id', 'name', 'symptoms', 'description', 'remedy', 'medications', 'products')

  symptoms = fields.List(fields.Nested('SymptomSchema'))
  medications = fields.List(fields.Nested('MedicationSchema'))
  products = fields.List(fields.Nested('ProductSchema'))

  
illness_schema = IllnessSchema()
illness_schema_many = IllnessSchema(many=True)