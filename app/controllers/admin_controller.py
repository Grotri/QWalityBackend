from flask import Blueprint, jsonify

from app.utils.role_required import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/ping", methods=["GET"])
@role_required("admin", "owner")
def ping():
    return jsonify({"msg": "Hello, admin!"})
