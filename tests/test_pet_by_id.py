def test_view_pet_happy_path_returns_200(auth_client, pet):
  # The owner can fetch their own pet by id and gets the serialized pet back.
  response = auth_client.get(f'/user/pets/{pet.id}')
  assert response.status_code == 200
  body = response.get_json()
  assert body['id'] == pet.id
  assert body['name'] == 'Rex'
