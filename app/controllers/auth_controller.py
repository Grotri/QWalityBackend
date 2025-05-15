import random

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_mail import Message

from app.extensions import mail, cache
from app.models import Client
from app.schemas.user.user_login_dto import UserLoginDTO
from app.usecases.user.login_user import LoginUserUseCase
from app.usecases.client.request_password_reset import RequestPasswordResetUseCase
from app.usecases.client.reset_password_confirm import ResetPasswordConfirmUseCase

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
    email = request.json.get("email")
    if not email:
        return jsonify({"error": "Email обязателен"}), 400

    # Пример проверки существующего пользователя
    if Client.query.filter_by(email=email).first():
        return jsonify({"error": "Пользователь уже существует"}), 400

    code = str(random.randint(100000, 999999))
    cache.set(f"reg_code:{email}", code, timeout=300)  # 5 минут

    msg = Message(
        subject="Подтверждение почты",
        recipients=[email],
        body=f"Ваш код подтверждения регистрации: {code}"
    )
    mail.send(msg)

    return jsonify({"message": "Код отправлен"}), 200


@auth_bp.route("/reset-password-request", methods=["POST"])
def request_reset():
    try:
        email = request.json.get("email")
        RequestPasswordResetUseCase.execute(email)
        return jsonify({"message": "Письмо отправлено"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/reset-password-confirm", methods=["POST"])
def confirm_reset():
    try:
        email = request.json.get("email")
        code = request.json.get("code")
        new_password = request.json.get("new_password")
        ResetPasswordConfirmUseCase.execute(email, code, new_password)
        return jsonify({"message": "Пароль обновлён"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
