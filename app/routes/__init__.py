from app.controllers.admin_controller import admin_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.user_controller import user_bp


def register_routes(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
