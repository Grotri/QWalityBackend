from flask import Blueprint, request, jsonify

from app.schemas.client.client_register_dto import ClientRegisterDTO
from app.usecases.client.register_client_usecase import RegisterClientUseCase

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.route("/", methods=["POST"])
def register_client():
    try:
        data = ClientRegisterDTO(**request.json)
        RegisterClientUseCase.execute(data)
        return jsonify({"message": "Клиент зарегистрирован"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 400
