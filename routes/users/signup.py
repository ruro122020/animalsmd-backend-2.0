from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models.models import User
from sqlalchemy.exc import IntegrityError
from marshmallow_schemas.users import user_schema

class Signup(Resource):
  def post(self):
    json = request.get_json()
    user = User(
      name=json.get('name'),
      username=json.get('username'),
      email=json.get('email'))
    
    user.password_hash = json.get('password')
 
    try:
      db.session.add(user)
      db.session.commit()
      session['user_id'] = user.id
      return user_schema.dump(user), 201
    except IntegrityError:
       return {'error': 'Unproccessable Entity'}, 422
    


api.add_resource(Signup, '/signup', endpoint='signup')