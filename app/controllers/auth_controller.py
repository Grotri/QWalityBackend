from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from app.schemas.auth.reset_password_confirm_dto import ResetPasswordConfirmDTO
from app.schemas.auth.reset_password_request_dto import ResetPasswordRequestDTO
from app.schemas.auth.send_registration_code_dto import SendRegistrationCodeDTO
from app.schemas.user.user_login_dto import UserLoginDTO
from app.usecases.auth.request_password_reset_usecase import RequestPasswordResetUseCase
from app.usecases.auth.reset_password_confirm_usecase import ResetPasswordConfirmUseCase
from app.usecases.auth.send_registration_code_usecase import SendRegistrationCodeUsecase
from app.usecases.user.login_user_usecase import LoginUserUseCase

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({
        "access_token": access_token
    }), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = UserLoginDTO(**request.json)
        tokens = LoginUserUseCase.execute(data)
        return jsonify(
            {"access_token": tokens["access_token"],
             "refresh_token": tokens["refresh_token"]}
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.route("/send-registration-code", methods=["POST"])
def send_registration_code():
    try:
        data = SendRegistrationCodeDTO(**request.json)
        SendRegistrationCodeUsecase.execute(data)

        return jsonify({"message": "Код отправлен"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/reset-password-request", methods=["POST"])
def request_reset():
    try:
        data = ResetPasswordRequestDTO(**request.json)
        RequestPasswordResetUseCase.execute(data)
        return jsonify({"message": "Письмо отправлено"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/reset-password-confirm", methods=["POST"])
def confirm_reset():
    try:
        data = ResetPasswordConfirmDTO(**request.json)
        ResetPasswordConfirmUseCase.execute(data)
        return jsonify({"message": "Пароль обновлён"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
