"""Functional tests for the cart collection resource at /user/cart."""

from models.models import Cart


def test_view_cart_happy_path_returns_200(auth_client, cart_item):
  response = auth_client.get('/user/cart')
  assert response.status_code == 200
  body = response.get_json()
  assert isinstance(body, list)
  ids = [item['id'] for item in body]
  assert cart_item.id in ids


def test_view_cart_empty_returns_200_empty_list(auth_client):
  response = auth_client.get('/user/cart')
  assert response.status_code == 200
  assert response.get_json() == []


def test_view_cart_unauthenticated_returns_401(client):
  response = client.get('/user/cart')
  assert response.status_code == 401


def test_add_to_cart_happy_path_returns_201(auth_client, csrf_token, product):
  response = auth_client.post(
    '/user/cart',
    json={'product_id': product.id, 'quantity': 3},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 201
  body = response.get_json()
  assert body['quantity'] == 3
  assert body['product']['id'] == product.id


def test_add_to_cart_product_already_in_cart_returns_409(
  auth_client, csrf_token, cart_item, product
):
  response = auth_client.post(
    '/user/cart',
    json={'product_id': product.id, 'quantity': 1},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 409


def test_add_to_cart_product_not_found_returns_404(auth_client, csrf_token):
  response = auth_client.post(
    '/user/cart',
    json={'product_id': 999999, 'quantity': 1},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 404


def test_add_to_cart_invalid_quantity_returns_422(
  auth_client, csrf_token, product
):
  response = auth_client.post(
    '/user/cart',
    json={'product_id': product.id, 'quantity': 0},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 422


def test_add_to_cart_unauthenticated_returns_401(client, csrf_token, product):
  response = client.post(
    '/user/cart',
    json={'product_id': product.id, 'quantity': 1},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 401


def test_clear_cart_happy_path_returns_200(
  auth_client, csrf_token, db_session, test_user, cart_item
):
  response = auth_client.delete(
    '/user/cart',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  remaining = Cart.query.filter_by(user_id=test_user.id).all()
  assert remaining == []


def test_clear_cart_already_empty_returns_200(auth_client, csrf_token):
  response = auth_client.delete(
    '/user/cart',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200


def test_clear_cart_unauthenticated_returns_401(client, csrf_token):
  response = client.delete(
    '/user/cart',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 401
