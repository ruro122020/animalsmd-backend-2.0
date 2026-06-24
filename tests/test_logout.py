def test_logout_when_logged_in_returns_200(auth_client, csrf_token):
  # A logged-in session can log out; the route clears user_id and returns an
  # empty body with 200.
  response = auth_client.delete(
    '/logout',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  assert response.get_json() == {}
