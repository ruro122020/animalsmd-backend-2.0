def test_pet_results_happy_path_returns_200(
  auth_client, db_session, pet, species, symptom
):
  # The results endpoint walks a full chain: the pet's symptom -> illnesses with
  # that symptom, intersected with illnesses whose classification matches the
  # pet's species classification. Build that chain so a matching illness exists.
  from models.models import (
    Illness,
    IllnessSymptom,
    Classification,
    SpeciesClassification,
    IllnessClassification,
    PetSymptom,
  )

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
