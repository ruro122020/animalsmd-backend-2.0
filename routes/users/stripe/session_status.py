
from config import api
from flask_restful import Resource
from flask import request, session
from models.models import User
import stripe


class SessionStatus(Resource):
  def get(self):
    # Require an authenticated user before touching Stripe at all.
    if not session.get('user_id'):
      return {"error": "Unauthorized"}, 401

    try:
      stripe_session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
      stripe_email = stripe_session.customer_details.email

      # Best-effort ownership check. Stripe checkout sessions are not linked to
      # users in our DB, so the only signal we have is the email on the session.
      # We compare it (case-insensitively) to the logged-in user's account email.
      user = User.query.filter_by(id=session.get('user_id')).first()
      if not user or not stripe_email or user.email.lower() != stripe_email.lower():
        return {"error": "Unauthorized"}, 403

      return {"status": stripe_session.status, "customer_email": stripe_email}, 200
    except Exception as e:
      return {"error": str(e)}, 400


api.add_resource(SessionStatus, '/user/session-status')
