from config import ma 
from models.models import Medication

class MedicationSchema(ma.Schema):
  class Meta:
    model = Medication
    load_instance = True
    fields = ('id', 'name', 'description')



medication_schema = MedicationSchema()
medication_schema_many = MedicationSchema(many=True)