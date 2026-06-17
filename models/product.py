from config import db
from .base import BaseModel

class Product(BaseModel):
  __tablename__='products'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  price = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String, nullable=False)
  prescription = db.Column(db.Boolean, nullable=False)

  #relationships
  carts = db.relationship('Cart', back_populates='product')

  illness_product = db.relationship('IllnessProduct', back_populates='product')

  #fields a client may change via update_db; never id or relationships
  updatable_fields = {'name', 'price', 'description', 'prescription'}

  #methods to communicate with database
  @classmethod
  def create_row(cls, name, price, description, prescription):
    product = cls(name=name, price=price, description=description, prescription=prescription)
    product.save_db()
    return product