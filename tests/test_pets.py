def test_list_pets_returns_only_current_users_pets(auth_client, pet, other_pet):
  # The list is scoped to the logged-in user, so test_user sees only their own
  # pet and never other_user's pet.
  response = auth_client.get('/user/pets')
  assert response.status_code == 200
  body = response.get_json()
  ids = [p['id'] for p in body]
  assert pet.id in ids
  assert other_pet.id not in ids


def test_list_pets_unauthenticated_returns_401(client):
  # The before_request auth hook is default-deny: without a logged-in session
  # the list endpoint must reject the request rather than leak any pets.
  response = client.get('/user/pets')
  assert response.status_code == 401


def test_create_pet_happy_path_returns_200(auth_client, csrf_token, species, symptom):
  # A complete body with a known species type and known symptom names creates the
  # pet, attaches its symptoms, and echoes the serialized pet back. CSRFProtect is
  # global so the mutating request must carry the X-CSRFToken header.
  response = auth_client.post(
    '/user/pets',
    json={
      'name': 'Buddy',
      'age': 2,
      'weight': 10,
      'type': 'dog',
      'symptoms': ['coughing'],
    },
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  body = response.get_json()
  assert body['name'] == 'Buddy'
  assert body['species_id'] == species.id
  symptom_names = [s['name'] for s in body['symptoms']]
  assert 'coughing' in symptom_names


def test_create_pet_missing_body_returns_400(auth_client, csrf_token):
  # An empty JSON object is falsy, so the route short-circuits with its own
  # "info missing" 400 before any species or symptom lookup.
  response = auth_client.post(
    '/user/pets',
    json={},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 400
  assert response.get_json() == {'error': 'User pet info missing'}


def test_create_pet_missing_species_type_returns_400(auth_client, csrf_token):
  # Without a `type` the route cannot resolve a species, so it rejects before
  # touching the database.
  response = auth_client.post(
    '/user/pets',
    json={'name': 'Buddy', 'age': 2, 'weight': 10, 'symptoms': ['coughing']},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 400
  assert response.get_json() == {'error': 'species type is missing'}


def test_create_pet_missing_symptoms_returns_400(auth_client, csrf_token):
  # Symptoms are required: a body with a type but no symptoms is rejected before
  # the duplicate-name and species lookups.
  response = auth_client.post(
    '/user/pets',
    json={'name': 'Buddy', 'age': 2, 'weight': 10, 'type': 'dog'},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 400
  assert response.get_json() == {'error': 'symptoms are missing'}


def test_create_pet_duplicate_name_returns_409(auth_client, csrf_token, pet, symptom):
  # Name uniqueness is scoped to the account. The `pet` fixture already owns a pet
  # named "Rex" for test_user, so reusing that name is a conflict.
  response = auth_client.post(
    '/user/pets',
    json={
      'name': 'Rex',
      'age': 1,
      'weight': 5,
      'type': 'dog',
      'symptoms': ['coughing'],
    },
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 409
  assert response.get_json() == {'error': 'Pet already Exist'}
