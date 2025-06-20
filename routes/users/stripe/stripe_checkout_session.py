#! /usr/bin/env python3.6
from itertools import product
from statistics import quantiles
from config import api
from flask_restful import Resource

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, jsonify, redirect, request

import stripe

class StripeCheckoutSession(Resource):
  def post(self):
  
    DOMAIN = os.getenv('DOMAIN')
    # This is your test secret API key.
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    product_list = request.get_json()
    
    line_items_list = []

    for product in product_list:
      product_obj = product.get('product')
      quantity = product.get('quantity')
      product_name = product_obj.get('name')
      product_price = product_obj.get('price')
      
      product_={
                "price_data": {
                  "currency": "usd",
                  "product_data": {"name": product_name},
                  "unit_amount": product_price * 100,
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
      return str(e)

    return jsonify(clientSecret=session.client_secret)




api.add_resource(StripeCheckoutSession, '/user/create-checkout-session')