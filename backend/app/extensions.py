from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
api = Api()
