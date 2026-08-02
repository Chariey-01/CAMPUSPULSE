from datetime import datetime

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import VisitPlan, Place
from app.utils.decorators import get_current_user


class VisitPlanListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        plans = VisitPlan.query.filter_by(user_id=current_user.id).all()
        return [p.to_dict() for p in plans], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        place_id = data.get("place_id")

        if not place_id:
            return {"error": "place_id is required"}, 400

        if Place.query.get(place_id) is None:
            return {"error": "place not found"}, 404

        current_user = get_current_user()

        plan = VisitPlan(
            user_id=current_user.id,
            place_id=place_id,
            status=data.get("status", "Planned"),
            notes=data.get("notes"),
        )
        db.session.add(plan)
        db.session.commit()

        return plan.to_dict(), 201


class VisitPlanResource(Resource):
    @jwt_required()
    def put(self, plan_id):
        plan = VisitPlan.query.get(plan_id)
        if plan is None:
            return {"error": "visit plan not found"}, 404

        current_user = get_current_user()
        if plan.user_id != current_user.id:
            return {"error": "you can only edit your own visit plans"}, 403

        data = request.get_json()

        if "status" in data:
            plan.status = data["status"]
            if data["status"] == "Visited" and plan.visited_at is None:
                plan.visited_at = datetime.utcnow()

        if "notes" in data:
            plan.notes = data["notes"]

        db.session.commit()
        return plan.to_dict(), 200

    @jwt_required()
    def delete(self, plan_id):
        plan = VisitPlan.query.get(plan_id)
        if plan is None:
            return {"error": "visit plan not found"}, 404

        current_user = get_current_user()
        if plan.user_id != current_user.id:
            return {"error": "you can only delete your own visit plans"}, 403

        db.session.delete(plan)
        db.session.commit()
        return {}, 204
