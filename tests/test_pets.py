def test_list_pets_returns_only_current_users_pets(auth_client, pet, other_pet):
  # The list is scoped to the logged-in user, so test_user sees only their own
  # pet and never other_user's pet.
  response = auth_client.get('/user/pets')
  assert response.status_code == 200
  body = response.get_json()
  ids = [p['id'] for p in body]
  assert pet.id in ids
  assert other_pet.id not in ids
