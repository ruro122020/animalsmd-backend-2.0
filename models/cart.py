from config import db
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BaseModel


class Cart(BaseModel):
  __tablename__ = 'carts'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
  quantity = db.Column(db.Integer, nullable=False)

  
  user = db.relationship('User', back_populates='carts')
  product = db.relationship('Product', back_populates='carts')
  
  #fields a client may change via update_db; prevents mass-assignment of
  #user_id/id/product_id from a raw request body
  updatable_fields = {'quantity'}

  #methods to communicate with database
  @classmethod
  def create_row(cls, user, product, quantity):
    cart = cls(user=user, product=product, quantity= quantity)
    cart.save_db()
    return cart