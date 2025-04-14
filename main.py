from flask import Flask
from flask_jwt_extended import JWTManager

from app.extensions import db
from app.routes import register_routes

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)

    register_routes(app)

    return app
