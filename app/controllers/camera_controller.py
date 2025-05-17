from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.repositories.camera_repository import CameraRepository
from app.schemas.camera.camera_create_dto import CameraCreateDTO
from app.schemas.camera.camera_update_dto import CameraUpdateDTO
from app.usecases.camera.add_camera_usecase import AddCameraUseCase
from app.usecases.camera.get_cameras_usecase import GetCamerasUseCase
from app.usecases.camera.update_camera_usecase import UpdateCameraUseCase
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
    try:
        cameras = GetCamerasUseCase.execute()
        return jsonify([
            {
                "id": cam.id,
                "name": cam.name,
                "camera_url": cam.camera_url,
                "status": cam.status,
                "created_at": cam.created_at.isoformat()
            } for cam in cameras
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@camera_bp.route("/<int:camera_id>", methods=["GET"])
@jwt_required()
def get_camera(camera_id):
    try:
        cam = CameraRepository.get_by_id(camera_id=camera_id)
        return jsonify(
            {
                "id": cam.id,
                "name": cam.name,
                "camera_url": cam.camera_url,
                "status": cam.status,
                "created_at": cam.created_at.isoformat()
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@camera_bp.route("/<int:camera_id>", methods=["PATCH"])
@jwt_required()
@role_required("owner", "admin", "moderator")
def update_camera(camera_id):
    try:
        data = CameraUpdateDTO(**request.json)
        answer = UpdateCameraUseCase.execute(camera_id, data)

        return jsonify({"message": str(answer)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# @camera_bp.route("/<int:camera_id>", methods=["DELETE"])
# @jwt_required()
# @role_required("owner", "admin")
# def delete_camera(camera_id):
#     try:
#         ans = DeleteCameraUseCase.execute(camera_id)
#
#         return jsonify({"message": str(ans)}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
