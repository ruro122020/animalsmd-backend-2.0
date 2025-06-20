
from config import ma
from models.models import Product

class ProductSchema(ma.Schema):
  class Meta:
    model: Product
    load_instance: True
    fields = ('id','name', 'price', 'description', 'prescription')

product_schema = ProductSchema()
product_schema_many = ProductSchema(many=True)