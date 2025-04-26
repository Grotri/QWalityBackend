from datetime import datetime

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User


class ResetPasswordConfirmUseCase:
    @staticmethod
    def execute(token: str, new_password: str):
        user = User.query.filter_by(reset_token=token).first()
        if not user or user.reset_token_expiry < datetime.utcnow():
            raise ValueError("Invalid or expired token")

        user.hashed_password = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
