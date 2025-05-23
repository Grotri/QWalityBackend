from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required

from app.utils.auth import get_current_user


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                user = get_current_user()
                if user.role not in allowed_roles:
                    return jsonify({"error": "У вас нет доступа к этому ресурсу"}), 403
                return fn(*args, **kwargs)
            except ValueError as e:
                return jsonify({"error": str(e)}), 401
            except Exception as e:
                return jsonify({"error": "Ошибка авторизации"}), 500

        return wrapper

    return decorator
