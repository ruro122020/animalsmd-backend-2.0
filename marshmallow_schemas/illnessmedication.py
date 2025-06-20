
from config import ma
from models.models import IllnessMedication
from flask_marshmallow.fields import fields


class IllnessMedicationSchema(ma.Schema):
  class Meta:
    model = IllnessMedication
    load_instance = True
  
  illness = fields.Nested('IllnessSchema')


illness_medication = IllnessMedicationSchema()
illness_medication_many = IllnessMedicationSchema(many=True)