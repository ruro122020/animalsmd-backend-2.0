from flask_restful import Resource
from config import api
from models.models import Product
from marshmallow_schemas.product import product_schema_many
class Products(Resource):
  def get(self):
    products = Product.query.all()
    if products:
      return product_schema_many.dump(products), 200
    return {"error": "Products do not exist"}, 400

api.add_resource(Products, '/products', endpoint='products')