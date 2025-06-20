from flask import request, session
from flask_restful import Resource
from config import api
from models.models import User
from marshmallow_schemas.users import user_schema

class Login(Resource):
  def post(self):
    json = request.get_json()
    user = User.query.filter(User.username == json.get('username')).first()

    if user:
      if user.authenticate(json.get('password')):
        session['user_id'] = user.id
        return user_schema.dump(user), 200
      else:
        return {'error':'Invalid Credentials'}, 401
    else:
      return {'error': 'User does NOT exist'}, 400


api.add_resource(Login, '/login', endpoint='login')