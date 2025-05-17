from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.repositories.camera_repository import CameraRepository
from app.repositories.defect_repository import DefectRepository
from app.utils.auth import get_current_client
from app.utils.serialize_defect import serialize_defect_with_product_and_inspection

defect_bp = Blueprint("defect", __name__, url_prefix="/defects")


@defect_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_defects():
    client = get_current_client()

    cameras = CameraRepository.get_all_by_client_id(client.id)
    cameras_defects = []
    for cam in cameras:
        defects = DefectRepository.get_all_with_inspections_and_products_by_camera_id_and_client_id(
            client_id=client.id,
            camera_id=cam.id
        )
        serialized_defects = [serialize_defect_with_product_and_inspection(d) for d in defects]

        cameras_defects.append({
            "camera_id": cam.id,
            "defects": serialized_defects
        })

    return jsonify(cameras_defects), 200


@defect_bp.route("/camera/<int:camera_id>", methods=["GET"])
@jwt_required()
def get_camera_defects(camera_id):
    client = get_current_client()

    defects = DefectRepository.get_all_with_inspections_and_products_by_camera_id_and_client_id(
        client_id=client.id,
        camera_id=camera_id
    )
    return jsonify([serialize_defect_with_product_and_inspection(d) for d in defects]), 200
