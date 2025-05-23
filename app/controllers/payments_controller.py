from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.schemas.payment.payment_create_dto import PaymentCreateDTO
from app.schemas.payment.payment_webhook_dto import PaymentWebhookDTO
from app.services.freekassa_client import FreeKassaClient
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
            sign=parsed.SIGN,
            ip=request.remote_addr  # Передаем IP для проверки
        )

        return "YES", 200  # FreeKassa ждёт именно ответ "YES"
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/status/<int:payment_id>", methods=["GET"])
@jwt_required()
def check_payment_status(payment_id):
    try:
        client = FreeKassaClient()
        status = client.check_payment_status(order_id=str(payment_id))
        return jsonify({"status": status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/balance", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_balance():
    try:
        client = FreeKassaClient()
        balance = client.get_balance()
        return jsonify({"balance": balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/history", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_payment_history():
    try:
        status = request.args.get("status")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        
        client = FreeKassaClient()
        orders = client.export_orders(
            status=status,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset
        )
        return jsonify({"orders": orders}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/shops", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_shops():
    try:
        client = FreeKassaClient()
        shops = client.get_shops()
        return jsonify({"shops": shops}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/payment-systems", methods=["GET"])
@jwt_required()
def get_payment_systems():
    try:
        client = FreeKassaClient()
        payment_systems = client.get_payment_systems()
        return jsonify({"payment_systems": payment_systems}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/payment-systems/<int:system_id>/check", methods=["GET"])
@jwt_required()
def check_payment_system(system_id):
    try:
        client = FreeKassaClient()
        status = client.check_payment_system(system_id)
        return jsonify({"status": status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/withdrawal-systems", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_withdrawal_systems():
    try:
        client = FreeKassaClient()
        withdrawal_systems = client.get_payment_systems_for_withdrawal()
        return jsonify({"withdrawal_systems": withdrawal_systems}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payments_bp.route("/withdrawal", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_withdrawal():
    try:
        data = request.json
        payment_system_id = data.get("payment_system_id")
        account = data.get("account")
        amount = float(data.get("amount"))
        currency = data.get("currency", "RUB")
        payment_id = data.get("payment_id")
        
        if not payment_system_id or not account or not amount:
            return jsonify({"error": "payment_system_id, account и amount обязательны"}), 400
        
        client = FreeKassaClient()
        result = client.create_withdrawal(
            payment_system_id=payment_system_id,
            account=account,
            amount=amount,
            currency=currency,
            payment_id=payment_id
        )
        
        return jsonify({"result": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
