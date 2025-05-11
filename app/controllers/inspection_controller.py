from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.schemas.inspect_product_dto import InspectProductDTO
from app.usecases.inspect_product import InspectProductUseCase

inspection_bp = Blueprint("inspections", __name__, url_prefix="/inspections")


@inspection_bp.route("/", methods=["POST"])
@jwt_required()
def inspect_product():
    try:
        form = {
            "batch_number": request.form["batch_number"],
            "camera_id": int(request.form["camera_id"]),
            "image": request.files["image"]
        }
        data = InspectProductDTO(**form)

        inspection, product, ai_result, image_url = InspectProductUseCase.execute(
            batch_number=data.batch_number,
            camera_id=data.camera_id,
            image=data.image
        )

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
