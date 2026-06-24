def test_signup_happy_path_returns_201(client, db_session, csrf_token):
  # A valid payload creates the user, returns 201 with the user JSON, and never
  # leaks the password back to the caller.
  response = client.post(
    '/signup',
    json={
      'name': 'Jane Doe',
      'username': 'janedoe',
      'email': 'janedoe@email.com',
      'password': 'supersecret',
    },
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 201
  body = response.get_json()
  assert body['username'] == 'janedoe'
  assert body['email'] == 'janedoe@email.com'
  assert 'password' not in body


def test_signup_empty_body_returns_400(client, csrf_token):
  # With no JSON body the route rejects the request before touching the model.
  response = client.post(
    '/signup',
    json={},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 400
  assert response.get_json() == {'error': 'Request body is required'}


def test_signup_missing_fields_returns_400(client, csrf_token):
  # A present but incomplete body is reported with the names of the fields that
  # are missing, before any model validation runs.
  response = client.post(
    '/signup',
    json={'username': 'janedoe'},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 400
  error = response.get_json()['error']
  assert error.startswith('Missing required fields:')
  assert 'name' in error
  assert 'email' in error
  assert 'password' in error


def test_signup_duplicate_user_returns_422(client, test_user, csrf_token):
  # Reusing an existing username trips the unique constraint, which the route
  # catches as an IntegrityError and reports as Unprocessable Entity.
  response = client.post(
    '/signup',
    json={
      'name': 'Impostor Smith',
      'username': 'jsmith',
      'email': 'different@email.com',
      'password': 'supersecret',
    },
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 422
  assert response.get_json() == {'error': 'Unproccessable Entity'}


def test_signup_invalid_name_returns_422(client, db_session, csrf_token):
  # The name validator requires a string longer than three characters; a short
  # name raises ValueError, which the route surfaces as a 422 with that message.
  response = client.post(
    '/signup',
    json={
      'name': 'Jo',
      'username': 'janedoe',
      'email': 'janedoe@email.com',
      'password': 'supersecret',
    },
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 422
  assert response.get_json() == {
    'error': 'Name must be of type string and more than 3 characters'
  }


def test_signup_invalid_email_returns_422(client, db_session, csrf_token):
  # The email validator rejects any value without an '@'; the resulting
  # ValueError is reported as a 422 with the validator's message.
  response = client.post(
    '/signup',
    json={
      'name': 'Jane Doe',
      'username': 'janedoe',
      'email': 'not-an-email',
      'password': 'supersecret',
    },
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 422
  assert response.get_json() == {'error': 'Email must be an email address'}
