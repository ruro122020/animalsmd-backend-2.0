from config import app
from models.models import Cart

with app.app_context():
  Cart.create_row(1, 2, 1)