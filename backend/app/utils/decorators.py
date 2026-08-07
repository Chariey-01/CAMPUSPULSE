from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

from app.models import User


def get_current_user():
    # assumes a JWT has already been verified (via @jwt_required or admin_required)
    # on the calling view - identity is stored as a string, hence the int() cast
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))


def admin_required(fn):
    # verifies the JWT itself, so use this INSTEAD OF @jwt_required() on a view,
    # not stacked alongside it
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"error": "admin access required"}, 403
        return fn(*args, **kwargs)
    return wrapper
