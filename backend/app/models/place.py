from app.extensions import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


class Place(db.Model, SerializerMixin):
    __tablename__ = "places"

    serialize_rules = (
        "-category.places",
        "-submitted_by_user",
        "-approved_by_user",
        "-reviews",
        "-visit_plans",
        "-bookmarks",
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    opening_hours = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    google_maps_link = db.Column(db.String(255))

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)  # one-to-many: Category -> Places
    submitted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # one-to-many: User -> submitted Places
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # set once an admin approves/rejects

    status = db.Column(db.String(20), nullable=False, default="Pending")  # Pending / Approved / Rejected
    approved_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship("Category", backref=db.backref("places", lazy="dynamic"))
    # two FKs to User, so foreign_keys= disambiguates which column each relationship joins on
    submitted_by_user = db.relationship(
        "User", foreign_keys=[submitted_by], backref=db.backref("places_submitted", lazy="dynamic")
    )
    approved_by_user = db.relationship(
        "User", foreign_keys=[approved_by], backref=db.backref("places_approved", lazy="dynamic")
    )

    def __repr__(self):
        return f"<Place {self.name}>"
