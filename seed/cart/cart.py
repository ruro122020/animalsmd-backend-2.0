from config import app
from models.models import Cart, User, Product

with app.app_context():
  user = User.query.filter_by(id=1).first()
  product = Product.query.filter_by(id=1).first()
  if user and product:
    Cart.create_row(user, product, 1)