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
