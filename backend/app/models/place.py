from app.extensions import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Place:
  __tablename__ = "places"

  serialize_rules = (
        "-category.places",
        "-submitted_by_user.places_submitted",
        "-approved_by_user.places_approved",
        "-reviews.place",
        "-visit_plans.place",
        "-bookmarks.place",
    )
# table columns on places table 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150), nullable=False)
  description = db.Column(db.Text)
  address = db.Column(db.String(255))
  phone = db.Column(db.String(20))
  opening_hours = db.Column(db.String(100))
  image_url = db.Column(db.String(255))
  google_maps_link = db.Column(db.String(255))

  #foreign keys on the places table 
  category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
  submitted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

  status = db.Column(db.String, nullable=False, default="Pending")
  approved_at = db.Column(db.DateTime, nullable=True)

  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

  category = db.relationship("Category", backref=db.backref("places", lazy="dynamic"))
  submitted_by = db.relationship(
    "User", foreign_keys[submitted_by],backref=db.backref("places_submitted", lazy="dynamic")
      )
  approved_by = db.Column(
    "Users", foreign_keys[approved_by], backref=db.backref("places_approved", lazy="dynamic")
    )


  def __repr__(self):
    return f"<Place {self.name}>"