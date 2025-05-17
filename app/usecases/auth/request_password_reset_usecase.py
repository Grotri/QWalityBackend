import random

from flask_mail import Message

from app.extensions import mail, cache
from app.repositories.user_repository import UserRepository
from app.schemas.auth.reset_password_request_dto import ResetPasswordRequestDTO


class RequestPasswordResetUseCase:
    @staticmethod
    def execute(dto: ResetPasswordRequestDTO):
        user = UserRepository.get_by_email(dto.email)
        if not user:
            raise ValueError("User not found")

        code = str(random.randint(100000, 999999))
        cache.set(f"reset_code:{dto.email}", code, timeout=300)

        msg = Message(
            subject="Восстановление пароля",
            recipients=[user.email],
            body=f"Ваш код для сброса пароля: {code}"
        )
        mail.send(msg)
