from config import ma
from models.models import Classification
from flask_marshmallow.fields import fields

class ClassificationSchema(ma.Schema):
  class Meta:
    model = Classification
    load_instance = True
  
  id = ma.Integer()
  classification = ma.String()


classification_schema = ClassificationSchema()
classifications_schema_many = ClassificationSchema(many=True)