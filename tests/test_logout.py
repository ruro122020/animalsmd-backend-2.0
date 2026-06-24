def test_logout_when_logged_in_returns_200(auth_client, csrf_token):
  # A logged-in session can log out; the route clears user_id and returns an
  # empty body with 200.
  response = auth_client.delete(
    '/logout',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  assert response.get_json() == {}


def test_logout_when_not_logged_in_returns_401(client, csrf_token):
  # With no user_id in the session there is nothing to log out, so the route
  # rejects the request with 401.
  response = client.delete(
    '/logout',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 401
  assert response.get_json() == {'error': 'not logged in'}
