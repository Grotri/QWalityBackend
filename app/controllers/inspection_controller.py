from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.schemas.inspection_create_dto import InspectionCreateDTO
from app.usecases.inspect_product import InspectProductUseCase

inspection_bp = Blueprint("inspections", __name__, url_prefix="/inspections")


@inspection_bp.route("/", methods=["POST"])
@jwt_required()
def inspect_product():
    try:
        data = InspectionCreateDTO(**request.json)
        inspection = InspectProductUseCase.execute(
            product_id=data.product_id,
            image_path=data.image_path  # временно, позже — файл
        )
        return jsonify({
            "id": inspection.id,
            "result": inspection.result,
            "defects_count": len(inspection.defects)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
