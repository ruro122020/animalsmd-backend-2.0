from flask import request, session
from flask_restful import Resource
from config import app, db, api, limiter
from models.models import User
from sqlalchemy.exc import IntegrityError
from marshmallow_schemas.users import user_schema

class Signup(Resource):
  decorators = [limiter.limit("5 per minute; 20 per hour")]

  def post(self):
    json = request.get_json()

    try:
      user = User(
        name=json.get('name'),
        username=json.get('username'),
        email=json.get('email'))
      user.password_hash = json.get('password')
      db.session.add(user)
      db.session.commit()
      session['user_id'] = user.id
      return user_schema.dump(user), 201
    except IntegrityError:
       db.session.rollback()
       return {'error': 'Unproccessable Entity'}, 422
    except ValueError as e:
       return {'error': str(e)}, 422
    


api.add_resource(Signup, '/signup', endpoint='signup')