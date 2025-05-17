from werkzeug.security import generate_password_hash

from app.extensions import cache
from app.repositories.user_repository import UserRepository
from app.schemas.auth.reset_password_confirm_dto import ResetPasswordConfirmDTO


class ResetPasswordConfirmUseCase:
    @staticmethod
    def execute(dto: ResetPasswordConfirmDTO):
        expected_code = cache.get(f"reset_code:{dto.email}")

        if int(expected_code) != int(dto.code):
            raise ValueError("Неверный код")

        user = UserRepository.get_by_email(dto.email)
        UserRepository.update(
            user.id,
            hashed_password=generate_password_hash(dto.new_password)
        )
