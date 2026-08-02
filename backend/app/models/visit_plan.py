from app.extensions import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


class VisitPlan(db.Model, SerializerMixin):
    __tablename__ = "visit_plans"

    serialize_rules = ("-user.visit_plans", "-place.visit_plans")

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"), nullable=False)

    status = db.Column(db.String(20), nullable=False, default="Planned")
    planned_date = db.Column(db.DateTime, nullable=True)
    visited_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("visit_plans", lazy="dynamic"))
    place = db.relationship("Place", backref=db.backref("visit_plans", lazy="dynamic"))

    def __repr__(self):
        return f"<VisitPlan user_id={self.user_id} place_id={self.place_id} status={self.status}>"
