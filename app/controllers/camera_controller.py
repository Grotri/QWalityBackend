from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Camera
from app.schemas.camera_create_dto import CameraCreateDTO
from app.usecases.add_camera import AddCameraUseCase
from app.utils.auth import get_current_user
from app.utils.license_limits import license_limited
from app.utils.role_required import role_required

camera_bp = Blueprint("cameras", __name__, url_prefix="/cameras")


@camera_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("owner", "admin", "moderator")
@license_limited("add_camera")
def add_camera():
    try:
        data = CameraCreateDTO(**request.json)
        camera = AddCameraUseCase.execute(data)
        return jsonify({
            "id": camera.id,
            "name": camera.name,
            "status": camera.status
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@camera_bp.route("/", methods=["GET"])
@jwt_required()
def get_cameras():
    user = get_current_user()
    status = request.args.get("status")  # optional: active, inactive, deleted

    query = Camera.query.filter_by(client_id=user.client_id)
    if status:
        query = query.filter_by(status=status)

    cameras = query.all()
    return jsonify([
        {
            "id": cam.id,
            "name": cam.name,
            "preview_url": cam.preview_url,
            "status": cam.status,
            "created_at": cam.created_at.isoformat()
        } for cam in cameras
    ]), 200


@camera_bp.route("/<int:camera_id>/status", methods=["PATCH"])
@jwt_required()
@role_required("owner", "admin", "moderator")
def update_camera_status(camera_id):
    user = get_current_user()
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ("active", "inactive", "deleted"):
        return jsonify({"error": "Invalid status"}), 400

    camera = Camera.query.filter_by(id=camera_id, client_id=user.client_id).first()
    if not camera:
        return jsonify({"error": "Camera not found"}), 404

    camera.status = new_status
    db.session.commit()

    return jsonify({"message": "Status updated", "status": camera.status}), 200


@camera_bp.route("/<int:camera_id>", methods=["DELETE"])
@jwt_required()
@role_required("owner", "admin")
def delete_camera(camera_id):
    user = get_current_user()
    camera = Camera.query.filter_by(id=camera_id, client_id=user.client_id).first()
    if not camera:
        return jsonify({"error": "Camera not found"}), 404

    camera.status = "deleted"
    db.session.commit()

    return jsonify({"message": "Camera marked as deleted"}), 200
