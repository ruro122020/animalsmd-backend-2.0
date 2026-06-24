def test_csrf_token_returns_usable_token(client):
  # The CSRF endpoint is public and must hand back a non-empty token string
  # that mutating requests can then echo back in the X-CSRFToken header.
  response = client.get('/csrf-token')
  assert response.status_code == 200
  token = response.get_json()['csrf_token']
  assert isinstance(token, str)
  assert token
