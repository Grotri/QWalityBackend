import random

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_mail import Message

from app.controllers import _build_cors_preflight_response, _corsify_actual_response
from app.extensions import mail, cache
from app.models import Client
from app.schemas.user_login_dto import UserLoginDTO
from app.usecases.login_user import LoginUserUseCase
from app.usecases.request_password_reset import RequestPasswordResetUseCase
from app.usecases.reset_password_confirm import ResetPasswordConfirmUseCase

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/refresh", methods=["POST", "OPTIONS"])
@jwt_required(refresh=True)
def refresh_token():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return _corsify_actual_response(jsonify({
            "access_token": access_token
        })), 200


@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            data = UserLoginDTO(**request.json)
            tokens = LoginUserUseCase.execute(data)
            return _corsify_actual_response(jsonify(
                {"access_token": tokens["access_token"],
                 "refresh_token": tokens["refresh_token"]}
            )), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 401


@auth_bp.route("/send-registration-code", methods=["POST", "OPTIONS"])
def send_registration_code():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    email = request.json.get("email")
    if not email:
        return jsonify({"error": "Email обязателен"}), 400

    # Пример проверки существующего пользователя
    if Client.query.filter_by(email=email).first():
        return jsonify({"error": "Пользователь уже существует"}), 400

    code = str(random.randint(100000, 999999))
    cache.set(f"reg_code:{email}", code, timeout=300)  # 5 минут
    print(code, cache.get(f"reg_code:{email}"))

    msg = Message(
        subject="Подтверждение почты",
        recipients=[email],
        body=f"Ваш код подтверждения регистрации: {code}"
    )
    mail.send(msg)

    return _corsify_actual_response(jsonify({"message": "Код отправлен"})), 200


@auth_bp.route("/reset-password-request", methods=["POST", "OPTIONS"])
def request_reset():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            email = request.json.get("email")
            RequestPasswordResetUseCase.execute(email)
            return _corsify_actual_response(jsonify({"message": "Письмо отправлено"})), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


@auth_bp.route("/reset-password-confirm", methods=["POST", "OPTIONS"])
def confirm_reset():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        try:
            email = request.json.get("email")
            code = request.json.get("code")
            new_password = request.json.get("new_password")
            ResetPasswordConfirmUseCase.execute(email, code, new_password)
            return _corsify_actual_response(jsonify({"message": "Пароль обновлён"})), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
