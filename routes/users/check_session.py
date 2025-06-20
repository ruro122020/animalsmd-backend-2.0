from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models.models import User
from marshmallow_schemas.users import user_schema

class CheckSession(Resource):
  def get(self):
    if session.get('user_id'):
      user = User.query.filter(User.id == session.get('user_id')).first()
      return user_schema.dump(user), 200
    return {}, 401
  

api.add_resource(CheckSession, '/check_session')