from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.schemas.payment.payment_create_dto import PaymentCreateDTO
from app.schemas.payment.payment_webhook_dto import PaymentWebhookDTO
from app.usecases.payment.create_payment_session_usecase import CreatePaymentSessionUseCase
from app.usecases.payment.handle_payment_webhook_usecase import HandlePaymentWebhookUseCase
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


@payments_bp.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        data = request.form or request.args  # может быть как POST, так и GET
        parsed = PaymentWebhookDTO(**data)

        HandlePaymentWebhookUseCase.execute(
            merchant_id=parsed.MERCHANT_ID,
            amount=parsed.AMOUNT,
            order_id=parsed.MERCHANT_ORDER_ID,
            sign=parsed.SIGN
        )

        return "YES", 200  # FreeKassa ждёт именно ответ "YES"
    except Exception as e:
        return jsonify({"error": str(e)}), 400
