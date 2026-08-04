from app.extensions import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


# many-to-many User <-> Place, plain join table (no extra data, unlike VisitPlan)
class Bookmark(db.Model, SerializerMixin):
    __tablename__ = "bookmarks"

    serialize_rules = ("-user.bookmarks", "-place.bookmarks")

    __table_args__ = (
        db.UniqueConstraint("user_id", "place_id", name="unique_user_place_bookmark"),  # can't bookmark twice
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("bookmarks", lazy="dynamic"))
    place = db.relationship("Place", backref=db.backref("bookmarks", lazy="dynamic"))

    def __repr__(self):
        return f"<Bookmark user_id={self.user_id} place_id={self.place_id}>"
