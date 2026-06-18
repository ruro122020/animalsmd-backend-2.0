import os

import pytest

# Importing config triggers Pipenv's automatic .env loading so the same
# USER/PASSWORD env vars the app uses are available here.
from config import app as flask_app, db


@pytest.fixture(scope='session')
def app():
  user = os.getenv('USER')
  password = os.getenv('PASSWORD')
  default_test_uri = (
    f'postgresql://{user}:{password}@localhost:5432/animalsmd_test'
  )
  test_uri = os.getenv('TEST_DATABASE_URL', default_test_uri)

  flask_app.config['SQLALCHEMY_DATABASE_URI'] = test_uri
  flask_app.config['TESTING'] = True
  flask_app.config['RATELIMIT_ENABLED'] = False
  flask_app.config['SESSION_COOKIE_SECURE'] = False

  with flask_app.app_context():
    db.create_all()
    yield flask_app
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def db_session(app):
  # Bind the session to a single connection-level transaction so every test
  # runs in isolation. Rolling back after the test discards all of its writes,
  # preventing state from leaking into other tests.
  connection = db.engine.connect()
  transaction = connection.begin()

  db.session.configure(bind=connection)

  yield db.session

  db.session.remove()
  transaction.rollback()
  connection.close()
  db.session.configure(bind=db.engine)


@pytest.fixture(scope='function')
def client(app):
  return app.test_client()


@pytest.fixture(scope='function')
def test_user(db_session):
  from models.models import User

  user = User(
    name='John Smith',
    username='jsmith',
    email='jsmith@email.com',
  )
  user.password_hash = 'testpassword123'
  db_session.add(user)
  db_session.commit()
  return user


@pytest.fixture(scope='function')
def csrf_token(client):
  response = client.get('/csrf-token')
  return response.get_json()['csrf_token']
