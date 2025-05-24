from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.repositories.user_repository import UserRepository
from app.schemas.user.update_user_role_dto import UpdateUserRoleDTO
from app.schemas.user.user_create_dto import UserCreateDTO
from app.usecases.user.create_sub_user_usecase import CreateSubUserUseCase
from app.usecases.user.delete_user_usecase import DeleteUserUseCase
from app.usecases.user.update_user_role_usecase import UpdateUserRoleUseCase
from app.utils.auth import get_current_user, get_current_client
from app.utils.role_required import role_required

user_bp = Blueprint("user", __name__, url_prefix="/users")


@user_bp.route("/<int:user_id>/role", methods=["PATCH"])
@role_required("admin", "owner")
def update_role(user_id):
    try:
        data = UpdateUserRoleDTO(**request.json)
        user = UpdateUserRoleUseCase.execute(user_id, data)
        return jsonify({
            "id": user.id,
            "login": user.login,
            "role": user.role
        })
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/sub-account", methods=["POST"])
@jwt_required()
@role_required("owner", "admin")
def create_sub_account():
    try:
        data = UserCreateDTO(**request.json)
        user = CreateSubUserUseCase.execute(data)
        return jsonify({
            "id": user.id,
            "login": user.login,
            "role": user.role
        }), 201
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("owner", "admin")
def list_users():
    client = get_current_client()
    users = UserRepository.get_all_by_client(client_id=client.id)
    return jsonify([
        {
            "id": u.id,
            "login": u.login,
            "role": u.role,
            "color_theme": u.color_theme,
            "font_size": u.font_size
        } for u in users
    ])


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    u = get_current_user()
    response_data = {
        "id": u.id,
        "login": u.login,
        "role": u.role,
        "color_theme": u.color_theme,
        "font_size": u.font_size
    }
    if u.role == "owner":
        client = get_current_client()
        if client:
            response_data["tin"] = client.tin
    return jsonify(response_data)


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required("owner", "admin")
def delete_user(user_id):
    try:
        DeleteUserUseCase.execute(user_id)
        return jsonify({"message": "User deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500
