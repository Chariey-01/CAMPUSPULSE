from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Review, Place
from app.utils.decorators import get_current_user


def _valid_rating(rating):
    return rating is not None and 1 <= int(rating) <= 5


class ReviewListResource(Resource):
    # GET /api/places/<id>/reviews - list reviews for a place (public)
    def get(self, place_id):
        place = Place.query.get(place_id)
        if place is None:
            return {"error": "place not found"}, 404

        reviews = Review.query.filter_by(place_id=place_id).all()
        return [r.to_dict() for r in reviews], 200

    # POST /api/places/<id>/reviews - post a review (rating 1-5)
    @jwt_required()
    def post(self, place_id):
        place = Place.query.get(place_id)
        if place is None:
            return {"error": "place not found"}, 404

        data = request.get_json()
        rating = data.get("rating")

        if not _valid_rating(rating):
            return {"error": "rating must be an integer between 1 and 5"}, 400

        current_user = get_current_user()

        review = Review(
            user_id=current_user.id,
            place_id=place_id,
            rating=rating,
            comment=data.get("comment"),
        )
        db.session.add(review)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "could not create review"}, 400

        return review.to_dict(), 201


class ReviewResource(Resource):
    # PUT /api/reviews/<id> - edit your own review
    @jwt_required()
    def put(self, review_id):
        review = Review.query.get(review_id)
        if review is None:
            return {"error": "review not found"}, 404

        current_user = get_current_user()
        if review.user_id != current_user.id:
            return {"error": "you can only edit your own reviews"}, 403

        data = request.get_json()

        if "rating" in data:
            if not _valid_rating(data["rating"]):
                return {"error": "rating must be an integer between 1 and 5"}, 400
            review.rating = data["rating"]

        if "comment" in data:
            review.comment = data["comment"]

        db.session.commit()
        return review.to_dict(), 200

    # DELETE /api/reviews/<id> - delete a review (owner or admin)
    @jwt_required()
    def delete(self, review_id):
        review = Review.query.get(review_id)
        if review is None:
            return {"error": "review not found"}, 404

        current_user = get_current_user()
        if review.user_id != current_user.id and current_user.role != "admin":
            return {"error": "you do not have permission to delete this review"}, 403

        db.session.delete(review)
        db.session.commit()
        return {}, 204
