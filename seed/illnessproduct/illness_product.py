from config import app
from models import product
from .illnesses_products_data import illness_product_data
from models.models import IllnessProduct, Illness, Product


def seed_illness_product_table():
   with app.app_context():
      for obj in illness_product_data:
        illness = Illness.query.filter_by(name = obj['illness']).first()
        for product_name in obj['products']:
          product = Product.query.filter_by(name = product_name).first()
          IllnessProduct.create_row(illness=illness, product=product)
   


seed_illness_product_table()