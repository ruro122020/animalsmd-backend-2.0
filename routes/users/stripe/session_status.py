
from config import api
from flask_restful import Resource
from flask import request
import stripe


class SessionStatus(Resource):
  def get(self):
    try:
      session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
      return {"status": session.status, "customer_email": session.customer_details.email}, 200
    except Exception as e:
      return {"error": str(e)}, 400


api.add_resource(SessionStatus, '/user/session-status')