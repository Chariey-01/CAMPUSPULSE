from app.extensions import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    serialize_rules = ("-user.reviews", "-place.reviews")

    # enforces rating range at the database level too, not just in the API layer
    __table_args__ = (
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # one-to-many: User -> Reviews
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"), nullable=False)  # one-to-many: Place -> Reviews

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("reviews", lazy="dynamic"))
    place = db.relationship("Place", backref=db.backref("reviews", lazy="dynamic"))

    def __repr__(self):
        return f"<Review place_id={self.place_id} rating={self.rating}>"
