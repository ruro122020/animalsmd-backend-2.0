from flask import session, jsonify, request
#Authentication is default-DENY: every endpoint requires a logged-in session
#unless its endpoint name is listed below. New endpoints are protected
#automatically, so forgetting to update this file fails safe (401) instead of
#silently exposing data.
public_routes = {
  'login', 'signup', 'logout', 'checksession', 'csrf_token',
  'products', 'product_by_id', 'species', 'speciesbytype',
  'testingroute', 'static',
}

class authenticate():
  def check_authentication():
    #let CORS preflight and unmatched routes (endpoint is None) through
    if request.method == 'OPTIONS' or request.endpoint is None:
      return None
    if request.endpoint in public_routes:
      return None
    if 'user_id' not in session:
      return jsonify({"Error": "Unauthorized"}), 401