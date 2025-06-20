from config import ma
from models.models import User
from flask_marshmallow.fields import fields

class UserSchema(ma.Schema):
  class Meta:
    model = User
    load_instance = True
    fields = ('id', 'name', 'email', 'username', 'cart_products')
  
  cart_products = fields.List(fields.Nested('ProductSchema'))


user_schema = UserSchema()
user_schema_many = UserSchema(many=True)