import traceback

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.controllers import _build_cors_preflight_response, _corsify_actual_response
from app.extensions import db
from app.models import User
from app.schemas.sub_user_create_dto import SubUserCreateDTO
from app.schemas.update_user_role_dto import UpdateUserRoleDTO
from app.usecases.create_sub_user import CreateSubUserUseCase
from app.usecases.update_user_role import UpdateUserRoleUseCase
from app.utils.auth import get_current_user
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
            "email": user.email,
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
        data = SubUserCreateDTO(**request.json)
        user = CreateSubUserUseCase.execute(data)
        return jsonify({
            "id": user.id,
            "email": user.email,
            "role": user.role
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("owner", "admin")
def list_users():
    current_user = get_current_user()
    users = User.query.filter_by(client_id=current_user.client_id).all()
    return jsonify([
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "color_theme": u.color_theme,
            "font_size": u.font_size
        } for u in users
    ])


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    u = get_current_user()
    return jsonify({
        "id": u.id,
        "email": u.email,
        "role": u.role,
        "color_theme": u.color_theme,
        "font_size": u.font_size
    })


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@role_required("owner", "admin")
def delete_user(user_id):
    # todo: rewrite into use case
    try:
        current_user = get_current_user()
        user = User.query.filter_by(id=user_id, client_id=current_user.client_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role in ["owner", "admin"] and current_user.role != "owner":
            return jsonify({"error": "Cannot delete users with this role"}), 403

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

    except Exception as e:
        print("🔥 Error in DELETE /users/<id>:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
