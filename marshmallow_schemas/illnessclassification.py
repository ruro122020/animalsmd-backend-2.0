from config import ma
from models.models import IllnessSymptom
from flask_marshmallow.fields import fields

class IllnessClassificationSchema(ma.Schema):
  class Meta:
    model:IllnessSymptom
    load_instance = True

  
  illness = fields.Nested("IllnessSchema")
  classification = fields.Nested('ClassificationSchema')
  id = ma.Integer()


illness_classification_schema = IllnessClassificationSchema()
illness_classification_schema_many = IllnessClassificationSchema(many=True)
