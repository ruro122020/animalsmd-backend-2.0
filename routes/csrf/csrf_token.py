from flask_restful import Resource
from flask_wtf.csrf import generate_csrf
from config import api

class CSRFToken(Resource):
  def get(self):
    token = generate_csrf()
    return {'csrf_token': token}, 200

api.add_resource(CSRFToken, '/csrf-token', endpoint='csrf_token')
