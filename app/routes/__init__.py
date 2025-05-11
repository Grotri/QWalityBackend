from app.controllers.admin_controller import admin_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.camera_controller import camera_bp
from app.controllers.client_controller import clients_bp
from app.controllers.defect_controller import defects_bp
from app.controllers.inspection_controller import inspection_bp
from app.controllers.minio_controller import utils_bp
from app.controllers.payments_controller import payments_bp
from app.controllers.user_controller import user_bp


def register_routes(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(camera_bp)
    app.register_blueprint(defects_bp)
    app.register_blueprint(utils_bp)
    app.register_blueprint(inspection_bp)
