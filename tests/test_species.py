"""Functional tests for the public species endpoints at /species."""


def test_list_species_happy_path_returns_200(client, species):
  # With a species row present, the list endpoint serializes and returns it.
  response = client.get('/species')
  assert response.status_code == 200
  ids = [item['id'] for item in response.get_json()]
  assert species.id in ids


def test_list_species_empty_returns_200_empty_list(client, db_session):
  # A successful read of an empty collection is 200 with an empty list, not 404.
  # /species is a valid collection that exists; having no rows is not a missing
  # resource. Currently fails: the route returns 404 {'error': 'No species found'}.
  response = client.get('/species')
  assert response.status_code == 200
  assert response.get_json() == []


def test_get_species_by_type_happy_path_returns_200(
  client, classification, species_classification, symptom_classification
):
  # The full chain (species -> species_classification -> classification ->
  # symptom_classification) resolves to the classification name and its symptoms.
  response = client.get('/species/dog')
  assert response.status_code == 200
  body = response.get_json()
  assert body['classification'] == 'mammal'
  assert 'coughing' in body['symptoms']
  assert body['classification_id'] == classification.id


def test_get_species_by_type_is_case_insensitive_returns_200(
  client, classification, species_classification, symptom_classification
):
  # The route lowercases type_name, so an uppercase request resolves the same row.
  response = client.get('/species/DOG')
  assert response.status_code == 200
  assert response.get_json()['classification'] == 'mammal'


def test_get_species_by_type_unknown_type_returns_404(client, db_session):
  # A type that maps to no species row short-circuits at the species lookup.
  response = client.get('/species/unicorn')
  assert response.status_code == 404
  assert response.get_json() == {'error': 'Species not found'}


def test_get_species_by_type_missing_species_classification_returns_500(client, species):
  # The species 'dog' exists, so this is not a missing resource (404). The request
  # fails because the server's own related data is incomplete, which is a
  # server-side data-integrity error -> 500. Currently fails: the route returns
  # 404 {'error': 'SpeciesClassification not found'}.
  response = client.get('/species/dog')
  assert response.status_code == 500


def test_get_species_by_type_missing_symptom_classification_returns_500(
  client, species_classification
):
  # Species, classification, and SpeciesClassification exist, so the addressed
  # species is present. Missing SymptomClassification rows are incomplete server
  # data, not a missing resource -> 500. Currently fails: the route returns
  # 404 {'error': 'SymptomClassification not found'}.
  response = client.get('/species/dog')
  assert response.status_code == 500
