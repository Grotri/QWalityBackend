from flask import Blueprint, request, jsonify

from app.schemas.update_user_role_dto import UpdateUserRoleDTO
from app.usecases.update_user_role import UpdateUserRoleUseCase
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
