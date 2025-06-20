from flask_restful import Resource
from config import api
from flask import request, session
from models.models import Cart, User, Product
from marshmallow_schemas.cart import cart_schema, cart_schema_many
from marshmallow_schemas.product import product_schema

class CartResource(Resource):
  def get(self):
    carts = Cart.query.filter_by(user_id=session.get('user_id')).order_by(Cart.id).all()
    if carts:
      return cart_schema_many.dump(carts), 200
    return {"error": "There are no products in user's cart"}

  def post(self):
    json = request.get_json()
    
    if json:
      try:
        #check if user exist
        user = User.query.filter_by(id=json.get('user_id')).first()
        if not user:
          return {"error": "user does not exist"}, 404
        #check if product exist
        product = Product.query.filter_by(id = json.get('product_id')).first()
        if not product:
          return {"error": "product does not exist"}
        
        #check if product already exist in user's cart
        if product in user.cart_products:          
          return {"error":"Product already exist in user's cart"},  403
        
        cart = Cart.create_row(user, product, json.get('quantity'))
        return cart_schema.dump(cart), 200
      except Exception as e:
        return {"error": str(e)}, 404
    return {"error": "Cart Not Added"}, 400
  
  def delete(self):
    user_session_id = session.get('user_id')
    if user_session_id:
      print(user_session_id)
      carts = Cart.query.filter_by(user_id = user_session_id).all()
      if carts:
        for cart in carts:
          cart.delete_db()
        return {}, 200
    return {"error": "Products don't exist"}, 400
    

api.add_resource(CartResource, '/user/cart', endpoint='user_cart')