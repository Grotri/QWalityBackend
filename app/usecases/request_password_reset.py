import secrets
from datetime import datetime, timedelta

from flask_mail import Message

from app.extensions import db, mail
from app.models.user import User


class RequestPasswordResetUseCase:
    @staticmethod
    def execute(email: str):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")

        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

        msg = Message(
            subject="Восстановление пароля",
            recipients=[user.email],
            body=f"Для восстановления пароля перейдите по ссылке:\n"
                 f"http://yourfrontend.com/reset-password?token={token}"
        )
        mail.send(msg)
