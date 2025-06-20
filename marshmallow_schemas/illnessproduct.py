from config import ma
from models.models import IllnessProduct
from flask_marshmallow.fields import fields

class IllnessProductSchema(ma.Schema):
  class Meta:
    model = IllnessProduct
    load_instance = True

  
  illness = fields.Nested('IllnessSchema')
  product = fields.Nested('ProductSchema')

illness_product_schema = IllnessProductSchema()
illness_product_many = IllnessProductSchema(many=True)