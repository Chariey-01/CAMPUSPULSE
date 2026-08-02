from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required

from app.extensions import db
from app.models import User, Profile
from app.utils.security import hash_password, verify_password
from app.utils.decorators import get_current_user


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "username, email, and password are required"}, 400

        if len(password) < 6:
            return {"error": "password must be at least 6 characters"}, 400

        if User.query.filter_by(username=username).first():
            return {"error": "username already taken"}, 409

        if User.query.filter_by(email=email).first():
            return {"error": "email already registered"}, 409

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        db.session.add(user)
        db.session.flush()  # assigns user.id without committing yet

        db.session.add(Profile(user_id=user.id))
        db.session.commit()

        return user.to_dict(), 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "username and password are required"}, 400

        user = User.query.filter_by(username=username).first()

        if user is None or not verify_password(user.password_hash, password):
            return {"error": "invalid username or password"}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )

        return {
            "access_token": access_token,
            "user": user.to_dict(),
        }, 200


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = get_current_user()
        return user.to_dict(), 200
