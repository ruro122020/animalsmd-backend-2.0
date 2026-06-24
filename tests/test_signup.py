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
