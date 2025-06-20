from config import ma
from models.models import Symptom
from flask_marshmallow.fields import fields

class SymptomSchema(ma.Schema):
  class Meta:
    model = Symptom
    load_instance = True

  id = ma.Integer()
  name = ma.String()

symptom_schema = SymptomSchema()
symptom_schema_many = SymptomSchema(many=True)