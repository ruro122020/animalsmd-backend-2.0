from config import db

class IllnessProduct(db.Model):
  __tablename__ = 'illnessesproducts'

  id = db.Column(db.Integer, primary_key=True)
  illness_id = db.Column(db.Integer, db.ForeignKey('illnesses.id'), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

  #relationships
  illness = db.relationship('Illness', back_populates='illness_product')
  product = db.relationship('Product', back_populates='illness_product')


  @classmethod
  def create_row(cls, illness, product):
    illness_product = cls(illness=illness, product=product)
    illness_product.save_db()
    return illness_product
  
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