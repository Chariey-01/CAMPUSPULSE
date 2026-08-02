from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.utils.decorators import get_current_user


class ProfileResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        return current_user.profile.to_dict(), 200

    @jwt_required()
    def put(self):
        current_user = get_current_user()
        profile = current_user.profile

        data = request.get_json()
        for field in ("bio", "avatar", "course", "year_of_study", "phone"):
            if field in data:
                setattr(profile, field, data[field])

        db.session.commit()
        return profile.to_dict(), 200
