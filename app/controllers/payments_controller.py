from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.schemas.payment_create_dto import PaymentCreateDTO
from app.usecases.create_payment_session import CreatePaymentSessionUseCase
from app.utils.role_required import role_required

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.route("/create-session", methods=["POST"])
@jwt_required()
@role_required("owner")
def create_payment_session():
    try:
        data = PaymentCreateDTO(**request.json)
        result = CreatePaymentSessionUseCase.execute(data.tariff_id)
        return jsonify(result), 201
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
