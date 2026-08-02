from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

from app.models import User


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"error": "admin access required"}, 403
        return fn(*args, **kwargs)
    return wrapper
