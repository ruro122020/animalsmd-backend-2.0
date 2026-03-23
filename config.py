# Standard library imports

# Remote library imports
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect

import os

#enviroment variables
  #postgresql local machine string:
  ##f'postgresql://{user}:{password}@localhost:5432/{dbname}'
  #local machine database credentials
user = os.getenv('USER')
password = os.getenv('PASSWORD')
dbname = os.getenv('DBNAME')

#supabase database
supauser = os.getenv('SUPAUSER')
supapassword =os.getenv('SUPAPASSWORD')
supadbname =os.getenv('SUPADBNAME')
supaport = os.getenv('SUPAPORT')

# Instantiate app, set attributes
app = Flask(__name__)

#Postgresql string
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@localhost:5432/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

#session key configuration
app.secret_key = os.getenv('SECRET_KEY')

# Cookie security
is_production = os.getenv('FLASK_ENV') != 'development'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = is_production
app.config['SESSION_COOKIE_SAMESITE'] = 'None' if is_production else 'Lax'

# CSRF token expiration (seconds)
app.config['WTF_CSRF_TIME_LIMIT'] = 3600

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
# migrate.init_app(app, db, render_as_batch=True)
db.init_app(app)

# Instantiate Marshmellow
ma = Marshmallow(app)

# Instantiate Bcrypt
bcrypt = Bcrypt(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
frontend_url = os.getenv('FRONTEND_URL')
CORS(app, supports_credentials=True, origins=[frontend_url])

# Instantiate CSRF protection
csrf = CSRFProtect(app)

