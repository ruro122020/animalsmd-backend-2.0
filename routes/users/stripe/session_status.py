
from config import api
from flask_restful import Resource
from flask import jsonify, request
import stripe


class SessionStatus(Resource):
  def get(self):
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    return jsonify(status=session.status, customer_email=session.customer_details.email)


api.add_resource(SessionStatus, '/user/session-status')