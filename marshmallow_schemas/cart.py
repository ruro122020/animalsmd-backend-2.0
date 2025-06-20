from config import ma
from models.models import Cart
from flask_marshmallow.fields import fields

class CartSchema(ma.Schema):
  class Meta:
    model = Cart
    load_instance=True
    fields = ('id', 'quantity', 'product')

  # user = fields.Nested('UserSchema')
  product = fields.Nested('ProductSchema')


cart_schema = CartSchema()
cart_schema_many = CartSchema(many=True)

