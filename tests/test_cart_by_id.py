"""Functional tests for the cart item resource at /user/cart/<id>."""

from models.models import Cart


def test_update_cart_item_happy_path_returns_200(
  auth_client, csrf_token, cart_item
):
  response = auth_client.patch(
    f'/user/cart/{cart_item.id}',
    json={'quantity': 5},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  assert response.get_json()['quantity'] == 5


def test_update_cart_item_not_found_returns_404(auth_client, csrf_token):
  response = auth_client.patch(
    '/user/cart/999999',
    json={'quantity': 5},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 404


def test_update_cart_item_owned_by_another_user_returns_403(
  auth_client, csrf_token, other_cart_item
):
  response = auth_client.patch(
    f'/user/cart/{other_cart_item.id}',
    json={'quantity': 9},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 403


def test_update_cart_item_unauthenticated_returns_401(
  client, csrf_token, cart_item
):
  response = client.patch(
    f'/user/cart/{cart_item.id}',
    json={'quantity': 5},
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 401


def test_delete_cart_item_happy_path_returns_200(
  auth_client, csrf_token, db_session, cart_item
):
  cart_item_id = cart_item.id
  response = auth_client.delete(
    f'/user/cart/{cart_item_id}',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 200
  assert db_session.get(Cart, cart_item_id) is None


def test_delete_cart_item_not_found_returns_404(auth_client, csrf_token):
  response = auth_client.delete(
    '/user/cart/999999',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 404


def test_delete_cart_item_owned_by_another_user_returns_403(
  auth_client, csrf_token, other_cart_item
):
  response = auth_client.delete(
    f'/user/cart/{other_cart_item.id}',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 403


def test_delete_cart_item_unauthenticated_returns_401(
  client, csrf_token, cart_item
):
  response = client.delete(
    f'/user/cart/{cart_item.id}',
    headers={'X-CSRFToken': csrf_token},
  )
  assert response.status_code == 401
