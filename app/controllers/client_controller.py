from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin

from app.controllers import _build_cors_preflight_response, _corsify_actual_response
from app.schemas.client_register_dto import ClientRegisterDTO
from app.usecases.register_client import RegisterClientUseCase

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.route("/", methods=["POST"])
# @clients_bp.route("/", methods=["POST", "OPTIONS"])
def register_client():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    try:
        data = ClientRegisterDTO(**request.json)
        RegisterClientUseCase.execute(data)
        return _corsify_actual_response(jsonify({"message": "Клиент зарегистрирован"})), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 400
