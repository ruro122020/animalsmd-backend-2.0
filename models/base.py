from config import db


class BaseModel(db.Model):
  #__abstract__ keeps SQLAlchemy from mapping BaseModel to its own table;
  #it only provides shared CRUD behavior to the models that inherit it.
  __abstract__ = True

  #fields a client may change via update_db. Empty by default so a model is
  #closed to mass-assignment until it deliberately opts fields in.
  updatable_fields = set()

  def save_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_db(self):
    db.session.delete(self)
    db.session.commit()

  def update_db(self, new_values):
    #Only whitelisted keys are written, and only when the value actually
    #differs. The set of changed fields is returned so a handler can tell a
    #real update from a no-op (the root cause behind issue #9's misleading 200s).
    changed = set()
    for key, value in new_values.items():
      if key in self.updatable_fields and getattr(self, key) != value:
        setattr(self, key, value)
        changed.add(key)
    if changed:
      db.session.commit()
    return changed
