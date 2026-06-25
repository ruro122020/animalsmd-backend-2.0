def test_view_pet_happy_path_returns_200(auth_client, pet):
  # The owner can fetch their own pet by id and gets the serialized pet back.
  response = auth_client.get(f'/user/pets/{pet.id}')
  assert response.status_code == 200
  body = response.get_json()
  assert body['id'] == pet.id
  assert body['name'] == 'Rex'


def test_view_pet_not_found_returns_404(auth_client):
  # An id that maps to no pet row returns 404 before any ownership check.
  response = auth_client.get('/user/pets/999999')
  assert response.status_code == 404
  assert response.get_json() == {'error': 'Pet does not exist'}


def test_view_pet_owned_by_another_user_returns_403(auth_client, other_pet):
  # The pet exists but belongs to other_user, so test_user is forbidden from
  # viewing it.
  response = auth_client.get(f'/user/pets/{other_pet.id}')
  assert response.status_code == 403
  assert response.get_json() == {'error': 'Unauthorized'}


def test_view_pet_unauthenticated_returns_401(client, pet):
  # The default-deny auth hook rejects an unauthenticated read even though the
  # pet exists.
  response = client.get(f'/user/pets/{pet.id}')
  assert response.status_code == 401


def test_update_pet_happy_path_returns_200(auth_client, csrf_token, pet):
  # Only name/age/weight are updatable. The request also tries to reassign user_id
  # and species_id, which the model whitelist must ignore to block mass-assignment.
  original_user_id = pet.user_id
  original_species_id = pet.species_id
  response = auth_client.patch(
    f'/user/pets/{pet.id}',
    json={
      'name': 'Rexy',
      'age': 4,
      'weight': 25,
      'user_id': 999,
      'species_id': 999,
    },
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  body = response.get_json()
  assert body['name'] == 'Rexy'
  assert body['age'] == 4
  assert body['weight'] == 25
  assert body['user_id'] == original_user_id
  assert body['species_id'] == original_species_id


def test_update_pet_not_found_returns_404(auth_client, csrf_token):
  # Patching a non-existent pet returns 404 before any field is touched.
  response = auth_client.patch(
    '/user/pets/999999',
    json={'name': 'Ghost'},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 404
  assert response.get_json() == {'error': 'Pet does not exist'}
