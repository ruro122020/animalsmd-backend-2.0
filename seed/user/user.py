from config import app, db
from models.user import User
from .users_data import users_data

def seed_users_table():
  with app.app_context():
    for user in users_data:
      user_exists = User.query.filter_by(username=user.get('username')).first()
      if not user_exists:
        new_user = User(
          name=user.get('name'),
          username=user.get('username'),
          email=user.get('email')
        )
        new_user.password_hash = user.get('password')
        db.session.add(new_user)
        db.session.commit()

seed_users_table()
