from itertools import product
from config import app
from models.models import Product
from .products_data import products_data

def seed_products_table():
  with app.app_context():
    for product in products_data:
      product_exists = Product.query.filter_by(name=product.get("name")).first()
      if not product_exists:
        Product.create_row(product.get("name"), product.get("price"), product.get("description"), product.get("prescription"))

seed_products_table()