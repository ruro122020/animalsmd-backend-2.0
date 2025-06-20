from itertools import product
from config import app
from models.models import Product
from .products_data import products_data

def seed_products_table():
  with app.app_context():
    Product.query.delete()
    for product in products_data:
      Product.create_row(product.get("name"), product.get("price"), product.get("description"), product.get("prescription")) 

seed_products_table()