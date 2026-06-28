"""Functional tests for the public product endpoints at /products."""


def test_list_products_happy_path_returns_200(client, product):
  response = client.get('/products')
  assert response.status_code == 200
  ids = [item['id'] for item in response.get_json()]
  assert product.id in ids


def test_list_products_empty_returns_400(client, db_session):
  response = client.get('/products')
  assert response.status_code == 400
  assert response.get_json() == {'error': 'Products do not exist'}
