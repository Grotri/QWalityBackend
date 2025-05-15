import random

from flask_mail import Message

from app.extensions import mail, cache
from app.repositories.user_repository import UserRepository


class RequestPasswordResetUseCase:
    @staticmethod
    def execute(email: str):
        user = UserRepository.get_by_email(email)
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
