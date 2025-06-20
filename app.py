
#!/usr/bin/env python3

# Local imports
from config import app
# Add your model imports
from routes.routes import *
from models.models import *
from utils.authenticate import authenticate

@app.before_request
def check_login():
  return authenticate.check_authentication()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
