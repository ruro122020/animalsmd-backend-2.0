from flask import request, session
from flask_restful import Resource
from config import api, limiter
from models.models import User
from marshmallow_schemas.users import user_schema

class Login(Resource):
  decorators = [limiter.limit("5 per minute; 20 per hour")]

  def post(self):
    json = request.get_json()
    if not json or not json.get('username') or not json.get('password'):
      return {'error': 'Invalid Credentials'}, 401
    user = User.query.filter(User.username == json.get('username')).first()

    #use one generic message for both cases so usernames can't be enumerated
    if user and user.authenticate(json.get('password')):
      session['user_id'] = user.id
      return user_schema.dump(user), 200
    return {'error': 'Invalid Credentials'}, 401


api.add_resource(Login, '/login', endpoint='login')