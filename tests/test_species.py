"""Functional tests for the public species endpoints at /species."""


def test_list_species_happy_path_returns_200(client, species):
  response = client.get('/species')
  assert response.status_code == 200
  ids = [item['id'] for item in response.get_json()]
  assert species.id in ids


def test_list_species_empty_returns_200_empty_list(client, db_session):
  response = client.get('/species')
  assert response.status_code == 200
  assert response.get_json() == []


def test_get_species_by_type_happy_path_returns_200(
  client, classification, species_classification, symptom_classification
):
  response = client.get('/species/dog')
  assert response.status_code == 200
  body = response.get_json()
  assert body['classification'] == 'mammal'
  assert 'coughing' in body['symptoms']
  assert body['classification_id'] == classification.id


def test_get_species_by_type_is_case_insensitive_returns_200(
  client, classification, species_classification, symptom_classification
):
  response = client.get('/species/DOG')
  assert response.status_code == 200
  assert response.get_json()['classification'] == 'mammal'


def test_get_species_by_type_unknown_type_returns_404(client, db_session):
  response = client.get('/species/unicorn')
  assert response.status_code == 404
  assert response.get_json() == {'error': 'Species not found'}


def test_get_species_by_type_missing_species_classification_returns_500(client, species):
  response = client.get('/species/dog')
  assert response.status_code == 500


def test_get_species_by_type_missing_symptom_classification_returns_500(
  client, species_classification
):
  response = client.get('/species/dog')
  assert response.status_code == 500
