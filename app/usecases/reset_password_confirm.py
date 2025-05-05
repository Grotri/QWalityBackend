from datetime import datetime

from flask import jsonify
from werkzeug.security import generate_password_hash

from app.extensions import db, cache
from app.models.user import User


class ResetPasswordConfirmUseCase:
    @staticmethod
    def execute(email: str, code: str, new_password: str):
        user = User.query.filter_by(email=email).first()
        print(user.email)

        expected_code = cache.get(f"reset_code:{email}")
        print(expected_code, code)
        if expected_code != code:
            raise ValueError("Неверный код")
        print(4)

        print(new_password)
        user.hashed_password = generate_password_hash(new_password)
        print(user.hashed_password)
        db.session.commit()
