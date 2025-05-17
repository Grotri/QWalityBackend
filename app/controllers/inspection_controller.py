import os
from io import BytesIO

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.datastructures import FileStorage

from app.schemas.inspection.inspect_product_dto import InspectProductDTO
from app.usecases.inspection.inspect_product_usecase import InspectProductUseCase

inspection_bp = Blueprint("inspections", __name__, url_prefix="/inspections")


@inspection_bp.route("/real/", methods=["POST"])
@jwt_required()
def inspect_product():
    try:
        print(1)
        form = {
            "camera_url": request.url,
            "batch_number": request.form["batch_number"],
            "camera_id": int(request.form["camera_id"]),
            "image": request.files["image"]
        }
        print(2)
        data = InspectProductDTO(**form)
        print(3)

        inspection, product, ai_result, image_url = InspectProductUseCase.execute(data)

        return jsonify({
            "inspection_id": inspection.id,
            "result": inspection.result,
            "product_id": product.id,
            "camera_id": product.camera_id,
            "image": image_url,
            "defects_count": len(ai_result.defects),
            "defects": ai_result.defects
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@inspection_bp.route("/test/", methods=["POST"])
@jwt_required()
def inspect_product():
    try:
        file_path = "./panel_19.jpg"
        if not os.path.exists(file_path):
            return {"error": f"File {file_path} not found"}, 400

        with open(file_path, "rb") as f:
            file_content = f.read()
        file_stream = BytesIO(file_content)
        file_name = os.path.basename(file_path)
        content_type = "image/jpeg"
        image_file = FileStorage(
            stream=file_stream,
            filename=file_name,
            content_type=content_type
        )

        print(1)
        form = {
            "camera_url": request.url,
            "batch_number": request.form["batch_number"],
            "camera_id": int(request.form["camera_id"]),
            "image": image_file
        }
        print(2)
        data = InspectProductDTO(**form)
        print(3)

        inspection, product, ai_result, image_url = InspectProductUseCase.execute(data)

        return jsonify({
            "inspection_id": inspection.id,
            "result": inspection.result,
            "product_id": product.id,
            "camera_id": product.camera_id,
            "image": image_url,
            "defects_count": len(ai_result.defects),
            "defects": ai_result.defects
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
