from config import db
from sqlalchemy.ext.hybrid import hybrid_property


class Cart(db.Model):
  __tablename__ = 'carts'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
  quantity = db.Column(db.Integer, nullable=False)

  
  user = db.relationship('User', back_populates='carts')
  product = db.relationship('Product', back_populates='carts')
  
  #methods to communicate with database
  @classmethod
  def create_row(cls, user, product, quantity):
    cart = cls(user=user, product=product, quantity= quantity)
    cart.save_db()
    return cart
  
  def save_db(self):
    db.session.add(self)
    db.session.commit()

  def update_db(self, new_values):
    for key, value in new_values.items():
      setattr(self, key, value)
    db.session.commit()

  def delete_db(self):
    db.session.delete(self)
    db.session.commit()