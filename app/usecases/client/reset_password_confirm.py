from werkzeug.security import generate_password_hash

from app.extensions import cache
from app.repositories.user_repository import UserRepository


class ResetPasswordConfirmUseCase:
    @staticmethod
    def execute(email: str, code: str, new_password: str):
        expected_code = cache.get(f"reset_code:{email}")
        if expected_code != code:
            raise ValueError("Неверный код")

        user = UserRepository.get_by_email(email)
        UserRepository.update(
            user.id,
            hashed_password=generate_password_hash(new_password)
        )