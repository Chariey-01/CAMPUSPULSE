from app.extensions import db
from sqlalchemy_serializer import SerializerMixin

class Category(db.Model, SerializerMixin):
  __tablename__ = "categories"

  serialize_rules = ("-places",)

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, unique=True)  # no duplicate category names
  icon = db.Column(db.String(255))
  description = db.Column(db.Text)
  # URL only - the app never stores image bytes in Postgres, so swapping the
  # source (an admin-entered link today, Cloudinary/Supabase Storage later)
  # never requires a schema or API change, just a different URL going in.
  hero_image = db.Column(db.String(500))

  def __repr__(self):
    return f"<Category {self.name}>"