def test_framework_and_auth_smoke(client, auth_client):
  # The CSRF endpoint is public and must hand back a usable token.
  csrf_response = client.get('/csrf-token')
  assert csrf_response.status_code == 200
  assert csrf_response.get_json()['csrf_token']

  # A logged-in client must reach a protected endpoint successfully.
  protected_response = auth_client.get('/check_session')
  assert protected_response.status_code == 200
