from flask import session, jsonify, request
#this file authenticates users before accessing protected routes.
#add route's endpoint to this array
protected_routes = ['user_pet_id', 'user_pet_results', 'user_cart' ]

class authenticate():
  def check_authentication():
    if 'user_id' not in session and request.endpoint in protected_routes:
      return jsonify({"Error":"Unauthorized"}), 401