from app.extensions import db
from sqlalchemy_serializer import SerializerMixin

class Category(db.Model, SerializerMixin):
  __tablename__ = "categories"

  serialize_rules = ("-places",)
# table columns on categories table
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, unique=True)
  icon = db.Column(db.String(255))
  description = db.Column(db.Text)

  def __repr__(self):
    return f"<Category {self.name}>"