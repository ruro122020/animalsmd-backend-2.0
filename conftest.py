import os

import pytest

# Importing config triggers Pipenv's automatic .env loading so the same
# USER/PASSWORD env vars the app uses are available here.
from config import app as flask_app, db

# Importing the app module wires up everything the real server does: it registers
# all models on db.metadata (so db.create_all() builds the full schema), mounts
# every route, and installs the auth before_request hook and CSRF error handler.
import app as _app_module  # noqa: F401


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
  # Run every test inside one connection-level transaction that is rolled back
  # at teardown, so no test's writes leak into another.
  #
  # Flask-SQLAlchemy's Session.get_bind always resolves ORM queries to
  # db.engines[None] and ignores the session's own bind, so binding the session
  # to a connection does nothing on its own. We swap db.engines[None] to point
  # at our single connection for the duration of the test, and set
  # join_transaction_mode='create_savepoint' so a test's commit() releases a
  # SAVEPOINT instead of committing the real transaction. The outer rollback
  # then discards everything.
  engines = db.engines
  original_engine = engines[None]
  connection = original_engine.connect()
  transaction = connection.begin()

  engines[None] = connection
  db.session.remove()
  db.session.configure(join_transaction_mode='create_savepoint')

  yield db.session

  db.session.remove()
  db.session.configure(join_transaction_mode='conditional_savepoint')
  engines[None] = original_engine
  transaction.rollback()
  connection.close()


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


@pytest.fixture(scope='function')
def auth_client(client, test_user, csrf_token):
  client.post(
    '/login',
    json={'username': 'jsmith', 'password': 'testpassword123'},
    headers={'X-CSRFToken': csrf_token},
  )
  return client
