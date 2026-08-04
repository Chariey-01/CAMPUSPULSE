from datetime import datetime

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Place, Category
from app.utils.decorators import admin_required, get_current_user
from app.utils.pagination import paginate_query
from app.services.place_service import attach_review_stats


class PlaceListResource(Resource):
    # GET /api/places - list approved places, with pagination/filter/search (public)
    def get(self):
        category_id = request.args.get("category_id", type=int)
        search = request.args.get("search")

        query = Place.query.filter_by(status="Approved")

        if category_id:
            query = query.filter_by(category_id=category_id)

        if search:
            query = query.filter(Place.name.ilike(f"%{search}%"))

        query = query.order_by(Place.created_at.desc())

        return paginate_query(query, serializer=attach_review_stats), 200

    # POST /api/places - submit a new place, always starts Pending
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_current_user()

        name = data.get("name")
        category_id = data.get("category_id")

        if not name or not category_id:
            return {"error": "name and category_id are required"}, 400

        if Category.query.get(category_id) is None:
            return {"error": "category does not exist"}, 404

        place = Place(
            name=name,
            description=data.get("description"),
            address=data.get("address"),
            phone=data.get("phone"),
            opening_hours=data.get("opening_hours"),
            image_url=data.get("image_url"),
            google_maps_link=data.get("google_maps_link"),
            category_id=category_id,
            submitted_by=current_user.id,
            status="Pending",
        )
        db.session.add(place)
        db.session.commit()

        return place.to_dict(), 201


class PlaceResource(Resource):
    # GET /api/places/<id> - get one place with review stats attached (public)
    def get(self, place_id):
        place = Place.query.get(place_id)
        if place is None:
            return {"error": "place not found"}, 404
        return attach_review_stats([place])[0], 200

    # PUT /api/places/<id> - update a place (owner or admin only)
    @jwt_required()
    def put(self, place_id):
        place = Place.query.get(place_id)
        if place is None:
            return {"error": "place not found"}, 404

        current_user = get_current_user()
        if place.submitted_by != current_user.id and current_user.role != "admin":
            return {"error": "you do not have permission to edit this place"}, 403

        data = request.get_json()
        for field in ("name", "description", "address", "phone", "opening_hours", "image_url", "google_maps_link"):
            if field in data:
                setattr(place, field, data[field])

        db.session.commit()
        return place.to_dict(), 200

    # DELETE /api/places/<id> - delete a place (owner or admin only)
    @jwt_required()
    def delete(self, place_id):
        place = Place.query.get(place_id)
        if place is None:
            return {"error": "place not found"}, 404

        current_user = get_current_user()
        if place.submitted_by != current_user.id and current_user.role != "admin":
            return {"error": "you do not have permission to delete this place"}, 403

        db.session.delete(place)
        db.session.commit()
        return {}, 204


class MyPlacesResource(Resource):
    # GET /api/places/mine - places the current user submitted, any status
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        query = Place.query.filter_by(submitted_by=current_user.id).order_by(Place.created_at.desc())
        return paginate_query(query), 200


class PendingPlacesResource(Resource):
    # GET /api/places/pending - admin moderation queue
    @admin_required
    def get(self):
        query = Place.query.filter_by(status="Pending").order_by(Place.created_at.asc())
        return paginate_query(query), 200


# shared by approve/reject below - only the resulting status differs
def _set_place_status(place_id, status):
    place = Place.query.get(place_id)
    if place is None:
        return {"error": "place not found"}, 404

    place.status = status
    place.approved_by = get_current_user().id
    place.approved_at = datetime.utcnow()
    db.session.commit()

    return place.to_dict(), 200


class PlaceApproveResource(Resource):
    # POST /api/places/<id>/approve - admin approves a pending place
    @admin_required
    def post(self, place_id):
        return _set_place_status(place_id, "Approved")


class PlaceRejectResource(Resource):
    # POST /api/places/<id>/reject - admin rejects a pending place
    @admin_required
    def post(self, place_id):
        return _set_place_status(place_id, "Rejected")
