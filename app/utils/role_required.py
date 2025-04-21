from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required

from app.utils.auth import get_current_user


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user.role not in allowed_roles:
                return jsonify({"error": "Access forbidden"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
