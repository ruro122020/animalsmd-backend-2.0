
#!/usr/bin/env python3

# Local imports
from flask import jsonify
from flask_wtf.csrf import CSRFError
from config import app
# Add your model imports
from routes.routes import *
from models.models import *
from utils.authenticate import authenticate

@app.before_request
def check_login():
  return authenticate.check_authentication()

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
  return jsonify({"error": "CSRF token missing or invalid"}), 400

if __name__ == '__main__':
    app.run(port=8000, debug=True)
