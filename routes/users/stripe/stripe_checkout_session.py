#! /usr/bin/env python3.6
from config import api
from flask_restful import Resource
from models.models import Product

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import request

import stripe

class StripeCheckoutSession(Resource):
  def post(self):
  
    DOMAIN = os.getenv('DOMAIN')
    # This is your test secret API key.
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    product_list = request.get_json()
    
    line_items_list = []

    if not isinstance(product_list, list) or not product_list:
      return {"error": "a non-empty list of products is required"}, 400

    for product in product_list:
      product_obj = product.get('product') if isinstance(product, dict) else None
      if not product_obj:
        return {"error": "each item must include a product"}, 400
      quantity = product.get('quantity')

      #look up the product server-side so price/name come from the DB, not the client
      db_product = Product.query.filter_by(id=product_obj.get('id')).first()
      if not db_product:
        return {"error": "product does not exist"}, 404

      product_={
                "price_data": {
                  "currency": "usd",
                  "product_data": {"name": db_product.name},
                  "unit_amount": db_product.price * 100,
                },
                "adjustable_quantity": {"enabled": True, "minimum": 1, "maximum": 10},
                "quantity": quantity,
              }
      line_items_list.append(product_)

    try:
      session = stripe.checkout.Session.create(
          ui_mode = 'embedded',
          line_items=line_items_list,
          mode='payment',
          return_url=DOMAIN + '/return?session_id={CHECKOUT_SESSION_ID}',
      )
    except Exception as e:
      return {"error": str(e)}, 400

    return {"clientSecret": session.client_secret}, 200




api.add_resource(StripeCheckoutSession, '/user/create-checkout-session')