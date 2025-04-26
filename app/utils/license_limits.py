from flask import jsonify
from functools import wraps
from app.models.user import User
from app.models.camera import Camera
from app.utils.license import get_active_license


class LicenseLimitError(Exception):
    pass


def license_limited(action):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            license = get_active_license()
            if not license:
                return jsonify({"error": "No active license"}), 403

            tariff = license.tariff

            # Проверка пользователей
            if action == "add_user":
                count = User.query.filter_by(client_id=license.client_id).count()
                if count >= tariff.user_limit:
                    raise LicenseLimitError("User limit exceeded")

            # Проверка ролей
            if action == "add_user":
                role = kwargs.get("role") or kwargs.get("data", {}).get("role")
                if role and role not in tariff.roles_allowed:
                    raise LicenseLimitError(f"Role '{role}' not allowed by current license")

            # Проверка камер
            if action == "add_camera":
                from app.models.camera import Camera  # avoid circular import
                count = Camera.query.filter_by(client_id=license.client_id).count()
                if tariff.camera_limit is not None and count >= tariff.camera_limit:
                    raise LicenseLimitError("Camera limit exceeded")

            return fn(*args, **kwargs)

        return wrapper

    return decorator
