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
