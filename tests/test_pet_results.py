from models.models import (
  Classification,
  Illness,
  IllnessClassification,
  IllnessSymptom,
  PetSymptom,
  SpeciesClassification,
)


def test_pet_results_happy_path_returns_200(
  auth_client, db_session, pet, species, symptom
):
  # The results endpoint walks a full chain: the pet's symptom -> illnesses with
  # that symptom, intersected with illnesses whose classification matches the
  # pet's species classification. Build that chain so a matching illness exists.
  PetSymptom.create_row(pet=pet, symptom=symptom)
  illness = Illness.create_row(
    name='Kennel Cough', description='A respiratory infection', remedy='Rest'
  )
  IllnessSymptom.create_row(illness=illness, symptom=symptom)
  classification = Classification.create_row(classification='mammal')
  SpeciesClassification.create(species=species, classification=classification)
  IllnessClassification.create_row(illness=illness, classification=classification)

  response = auth_client.get(f'/user/pets/{pet.id}/results')
  assert response.status_code == 200
  names = [illness['name'] for illness in response.get_json()]
  assert 'Kennel Cough' in names


def test_pet_results_pet_not_found_returns_400(auth_client):
  # The results endpoint reports a missing pet with 400 (not 404, unlike the other
  # pet-by-id routes), short-circuiting before any classification lookup.
  response = auth_client.get('/user/pets/999999/results')
  assert response.status_code == 400
  assert response.get_json() == {'error': 'pet id not found or pet does not exist'}


def test_pet_results_owned_by_another_user_returns_403(auth_client, other_pet):
  # The ownership check runs before any classification work, so requesting another
  # user's pet results is forbidden.
  response = auth_client.get(f'/user/pets/{other_pet.id}/results')
  assert response.status_code == 403
  assert response.get_json() == {'error': 'Unauthorized'}


def test_pet_results_no_matching_illnesses_returns_404(
  auth_client, db_session, pet, species
):
  # The pet's species needs a classification so the lookup does not crash, but the
  # pet has no symptoms, so no illness matches and the endpoint reports 404.
  classification = Classification.create_row(classification='mammal')
  SpeciesClassification.create(species=species, classification=classification)

  response = auth_client.get(f'/user/pets/{pet.id}/results')
  assert response.status_code == 404
  assert response.get_json() == {'error': 'No Results found'}


def test_pet_results_unauthenticated_returns_401(client, pet):
  # The default-deny auth hook blocks the results endpoint for an unauthenticated
  # session even though the pet exists.
  response = client.get(f'/user/pets/{pet.id}/results')
  assert response.status_code == 401
