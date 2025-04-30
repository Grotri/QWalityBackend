from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from app.config import Config
from app.schemas.user_create_dto import UserCreateDTO
from app.schemas.user_login_dto import UserLoginDTO
from app.usecases.login_user import LoginUserUseCase
from app.usecases.register_user import RegisterUserUseCase
from app.usecases.request_password_reset import RequestPasswordResetUseCase
from app.usecases.reset_password_confirm import ResetPasswordConfirmUseCase

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({
        "access_token": access_token
    }), 200


if Config.FLASK_ENV == "development":
    @auth_bp.route("/register", methods=["POST"])
    def register():
        try:
            data = UserCreateDTO(**request.json)
            user = RegisterUserUseCase.execute(data)
            return jsonify({
                "id": user.id,
                "email": user.email,
                "role": user.role
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400


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
        token = request.json.get("token")
        new_password = request.json.get("password")
        ResetPasswordConfirmUseCase.execute(token, new_password)
        return jsonify({"message": "Пароль обновлён"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
