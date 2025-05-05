import random

from flask_mail import Message

from app.extensions import mail, cache
from app.models.user import User


class RequestPasswordResetUseCase:
    @staticmethod
    def execute(email: str):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")

        code = str(random.randint(100000, 999999))
        cache.set(f"reset_code:{email}", code, timeout=300)

        msg = Message(
            subject="Восстановление пароля",
            recipients=[user.email],
            body=f"Ваш код для сброса пароля: {code}"
        )
        mail.send(msg)
