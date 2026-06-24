from conftest import TEST_USERNAME


def test_check_session_authenticated_returns_200(auth_client):
  # A logged-in client gets its own user JSON back from the session check.
  response = auth_client.get('/check_session')
  assert response.status_code == 200
  body = response.get_json()
  assert body['username'] == TEST_USERNAME
  assert 'password' not in body
