import random

from flask_mail import Message

from app.extensions import cache, mail
from app.repositories.client_repository import ClientRepository
from app.schemas.auth.send_registration_code_dto import SendRegistrationCodeDTO


class SendRegistrationCodeUsecase:
    @staticmethod
    def execute(dto: SendRegistrationCodeDTO):
        if not dto.email:
            raise ValueError("Email обязателен")

        if ClientRepository.get_by_email(dto.email):
            raise ValueError("Пользователь уже существует")

        code = str(random.randint(100000, 999999))
        cache.set(f"reg_code:{dto.email}", code, timeout=300)  # 5 минут

        msg = Message(
            subject="Подтверждение почты",
            recipients=[dto.email],
            body=f"Ваш код подтверждения регистрации: {code}"
        )
        mail.send(msg)
