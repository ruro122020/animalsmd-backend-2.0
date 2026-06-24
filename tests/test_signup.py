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
