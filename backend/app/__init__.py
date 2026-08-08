import os

import cloudinary
from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt, cors, api


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # Falls back to "*" (any origin) when FRONTEND_URL is unset - fine for local dev(frontend url is always in .env) but should be set in production for security.
    cors.init_app(app, resources={r"/api/.*": {"origins": os.getenv("FRONTEND_URL", "*")}})

    # No Flask extension wrapper for this SDK - it just holds config as module-level
    # state once set, which app/utils/uploads.py then reads at signature-generation time.
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
        secure=True,
    )

    # Must be imported (even though unused directly) before Flask-Migrate/SQLAlchemy
    # can see the model metadata needed for `flask db migrate` autogeneration.
    from app import models  # noqa: F401

    from app.resources import register_resources
    register_resources(api)
    api.init_app(app)

    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    @app.get("/")
    def home():
        return {
            "message": "Welcome to CampusPulse API",
            "status": "running"
        }

    return app
