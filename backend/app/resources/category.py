from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Category
from app.utils.decorators import admin_required


class CategoryListResource(Resource):
    # GET /api/categories - list all categories (public)
    def get(self):
        categories = Category.query.all()
        return [c.to_dict() for c in categories], 200

    # POST /api/categories - create a category (admin only)
    @admin_required
    def post(self):
        data = request.get_json()
        name = data.get("name")

        if not name:
            return {"error": "name is required"}, 400

        if Category.query.filter_by(name=name).first():
            return {"error": "category already exists"}, 409

        category = Category(
            name=name,
            icon=data.get("icon"),
            description=data.get("description"),
        )
        db.session.add(category)
        db.session.commit()

        return category.to_dict(), 201


class CategoryResource(Resource):
    # GET /api/categories/<id> - get one category (public)
    def get(self, category_id):
        category = Category.query.get(category_id)
        if category is None:
            return {"error": "category not found"}, 404
        return category.to_dict(), 200

    # PUT /api/categories/<id> - update a category (admin only)
    @admin_required
    def put(self, category_id):
        category = Category.query.get(category_id)
        if category is None:
            return {"error": "category not found"}, 404

        data = request.get_json()
        category.name = data.get("name", category.name)
        category.icon = data.get("icon", category.icon)
        category.description = data.get("description", category.description)
        db.session.commit()

        return category.to_dict(), 200

    # DELETE /api/categories/<id> - delete a category (admin only)
    @admin_required
    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category is None:
            return {"error": "category not found"}, 404

        try:
            db.session.delete(category)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # blocked by FK constraint if places still reference this category
            return {"error": "cannot delete a category that still has places assigned to it"}, 409

        return {}, 204
