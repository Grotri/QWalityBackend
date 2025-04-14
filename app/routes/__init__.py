from app.controllers.auth_controller import auth_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
