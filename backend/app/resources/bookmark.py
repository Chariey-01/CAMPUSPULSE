from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Bookmark, Place
from app.utils.decorators import get_current_user


class BookmarkListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
        return [b.to_dict() for b in bookmarks], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        place_id = data.get("place_id")

        if not place_id:
            return {"error": "place_id is required"}, 400

        if Place.query.get(place_id) is None:
            return {"error": "place not found"}, 404

        current_user = get_current_user()

        bookmark = Bookmark(user_id=current_user.id, place_id=place_id)
        db.session.add(bookmark)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "place already bookmarked"}, 409

        return bookmark.to_dict(), 201


class BookmarkResource(Resource):
    @jwt_required()
    def delete(self, bookmark_id):
        bookmark = Bookmark.query.get(bookmark_id)
        if bookmark is None:
            return {"error": "bookmark not found"}, 404

        current_user = get_current_user()
        if bookmark.user_id != current_user.id:
            return {"error": "you can only remove your own bookmarks"}, 403

        db.session.delete(bookmark)
        db.session.commit()
        return {}, 204
