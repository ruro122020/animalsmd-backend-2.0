from conftest import TEST_USERNAME, TEST_PASSWORD


def test_login_valid_credentials_returns_200(client, test_user, csrf_token):
  # Correct username and password log the user in and return their JSON, without
  # ever echoing the password back.
  response = client.post(
    '/login',
    json={'username': TEST_USERNAME, 'password': TEST_PASSWORD},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  body = response.get_json()
  assert body['username'] == TEST_USERNAME
  assert 'password' not in body


def test_login_wrong_password_returns_401(client, test_user, csrf_token):
  # A real username with the wrong password is rejected with the same generic
  # message used for unknown users, so usernames cannot be enumerated.
  response = client.post(
    '/login',
    json={'username': TEST_USERNAME, 'password': 'wrongpassword'},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 401
  assert response.get_json() == {'error': 'Invalid Credentials'}


def test_login_missing_credentials_returns_401(client, csrf_token):
  # A body that omits the password short-circuits to the same generic rejection
  # before any user lookup happens.
  response = client.post(
    '/login',
    json={'username': TEST_USERNAME},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 401
  assert response.get_json() == {'error': 'Invalid Credentials'}
