from flask_restful import Resource
from config import api
from models.models import Cart
from flask import request
from marshmallow_schemas.cart import cart_schema

class CartByID(Resource):
  def patch(self, id):
    json = request.get_json()
    cart = Cart.query.filter_by(id=id).first()
    if not cart:
      return {"error": "Cart does not exist"}, 400
    
    cart.update_db(json)
    return cart_schema.dump(cart), 200

  def delete(self, id):
    cart = Cart.query.filter_by(id=id).first()
    if not cart:
      return {"error": "Cart does not exist"}, 400
    
    cart.delete_db()
    return {}, 200
    



api.add_resource(CartByID, '/user/cart/<int:id>')
