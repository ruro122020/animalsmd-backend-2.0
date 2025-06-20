from config import ma
from models.models import SymptomClassification
from flask_marshmallow.fields import fields

class SymptomClassificationSchema(ma.Schema):
  class Meta:
    model = SymptomClassification
    load_instance = True

  classification = fields.Nested("ClassificationSchema")
  symptom = fields.Nested("SymptomSchema")
  id = ma.Integer()



symptom_classification_schema=SymptomClassificationSchema()
symptom_classification_schema_many=SymptomClassificationSchema(many=True)