from config import ma
from models.models import IllnessSymptom
from flask_marshmallow.fields import fields

class IllnessSymptomSchema(ma.Schema):
  class Meta:
    model:IllnessSymptom
    load_instance = True

  
  illness = fields.Nested("IllnessSchema")
  # symptom = fields.Nested('SymptomSchema')
  # id = ma.Integer()


illness_symptom_schema = IllnessSymptomSchema()
illness_symptom_schema_many = IllnessSymptomSchema(many=True)




