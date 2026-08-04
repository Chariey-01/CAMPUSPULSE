from app.extensions import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = (
        "-password_hash",  # never serialize the hash
        "-profile.user",
        "-reviews",
        "-places_submitted",
        "-places_approved",
        "-visit_plans",
        "-bookmarks",
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)  # set via werkzeug generate_password_hash
    role = db.Column(db.String(20), nullable=False, default="student")  # "student" or "admin"
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

