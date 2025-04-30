from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.minio_client import MinioClient
from app.usecases.inspect_product import InspectProductUseCase

inspection_bp = Blueprint("inspections", __name__, url_prefix="/inspections")


@inspection_bp.route("/", methods=["POST"])
@jwt_required()
def inspect_product():
    try:
        product_id = request.form["product_id"]
        file = request.files["image"]

        if not file:
            return jsonify({"error": "Image file required"}), 400

        minio = MinioClient()
        image_url = minio.upload_file(file.stream, file.filename)

        inspection = InspectProductUseCase.execute(
            product_id=int(product_id),
            image_path=image_url  # теперь URL, не локальный путь
        )
        return jsonify({
            "id": inspection.id,
            "result": inspection.result,
            "defects_count": len(inspection.defects),
            "image": image_url
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
