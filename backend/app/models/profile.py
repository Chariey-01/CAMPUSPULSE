from app.extensions import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    course = db.Column(db.String(100))
    year_of_study = db.Column(db.Integer)
    phone = db.Column(db.String(20))

    user = db.relationship("User", backref=db.backref("profile", uselist=False))

    def __repr__(self):
        return f"<Profile user_id={self.user_id}>"
