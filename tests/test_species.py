"""Functional tests for the public species endpoints at /species."""


def test_list_species_happy_path_returns_200(client, species):
  # With a species row present, the list endpoint serializes and returns it.
  response = client.get('/species')
  assert response.status_code == 200
  ids = [item['id'] for item in response.get_json()]
  assert species.id in ids


def test_list_species_empty_returns_404(client, db_session):
  # With no species rows, the endpoint reports the empty table as a 404.
  response = client.get('/species')
  assert response.status_code == 404
  assert response.get_json() == {'error': 'No species found'}
