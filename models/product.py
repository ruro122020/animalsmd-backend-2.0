from config import db

class Product(db.Model):
  __tablename__='products'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  price = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String, nullable=False)
  prescription = db.Column(db.Boolean, nullable=False)

  #relationships
  carts = db.relationship('Cart', back_populates='product')

  illness_product = db.relationship('IllnessProduct', back_populates='product')
  
  #methods to communicate with database
  @classmethod
  def create_row(cls, name, price, description, prescription):
    product = cls(name=name, price=price, description=description, prescription=prescription)
    product.save_db()
    return product
  
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