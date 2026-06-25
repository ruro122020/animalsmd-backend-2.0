import os

import pytest

# Importing config triggers Pipenv's automatic .env loading so the same
# USER/PASSWORD env vars the app uses are available here.
from config import app as flask_app, db, limiter

# Importing the app module wires up everything the real server does: it registers
# all models on db.metadata (so db.create_all() builds the full schema), mounts
# every route, and installs the auth before_request hook and CSRF error handler.
import app as _app_module

# Single source of truth for the test login. test_user inserts this user and
# auth_client logs in with these same credentials. Keeping them here avoids
# duplicating the literals across fixtures where a typo would silently break login.
TEST_USERNAME = 'jsmith'
TEST_PASSWORD = 'testpassword123'


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
  # Disable the rate limiter for the whole suite. auth_client is function scoped,
  # so it logs in once per test, and POST /login is capped at 5/min, 20/hour. Left
  # enabled, the suite would trip 429 Too Many Requests and produce flaky failures
  # unrelated to the code under test. The tradeoff is that the limiter itself goes
  # uncovered here, so it needs a dedicated test that re-enables it locally.
  #
  # Flask-Limiter caches its enabled flag from RATELIMIT_ENABLED at construction
  # time, which happens on import in config.py before this fixture runs, so
  # setting the config key alone has no effect. Set limiter.enabled directly so
  # the limit decorators become no-ops for the suite.
  flask_app.config['RATELIMIT_ENABLED'] = False
  limiter.enabled = False
  flask_app.config['SESSION_COOKIE_SECURE'] = False

  with flask_app.app_context():
    db.create_all()
    yield flask_app
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def app_context(app):
  # Push a fresh application context per test so Flask's `g` starts empty each
  # time. The session-scoped `app` fixture keeps one long-lived context open for
  # create_all/drop_all, and `g` is bound to the application context, so without
  # a per-test context every test would share the same `g`. flask_wtf's
  # generate_csrf caches its token in `g` and only writes the matching value to
  # the session when it is absent; a leaked `g.csrf_token` makes the second test
  # onward skip that session write, emit no session cookie, and fail CSRF
  # validation on the next mutating request. A nested context gives each test its
  # own `g` and is popped at teardown.
  with app.app_context():
    yield


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
    username=TEST_USERNAME,
    email='jsmith@email.com',
  )
  user.password_hash = TEST_PASSWORD
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
    json={'username': TEST_USERNAME, 'password': TEST_PASSWORD},
    headers={'X-CSRFToken': csrf_token},
  )
  return client


@pytest.fixture(scope='function')
def species(db_session):
  # A single species row used to back pet fixtures and create requests. The
  # type_name is lowercase because the create-pet route lowercases the incoming
  # `type` before looking the species up.
  from models.models import Species

  return Species.create_row(type_name='dog')


@pytest.fixture(scope='function')
def symptom(db_session):
  # A single symptom row used to attach to pets and to resolve symptom names in
  # create-pet requests.
  from models.models import Symptom

  return Symptom.create_row(name='coughing')


@pytest.fixture(scope='function')
def pet(db_session, test_user, species):
  # A pet owned by test_user, so auth_client (logged in as test_user) is its
  # owner. create_row takes the species and user as IDs.
  from models.models import Pet

  return Pet.create_row(
    name='Rex', age=3, weight=20, species=species.id, user=test_user.id
  )
