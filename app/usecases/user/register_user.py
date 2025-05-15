from werkzeug.security import generate_password_hash

from app.repositories.user_repository import UserRepository
from app.schemas.user.user_create_dto import UserCreateDTO


class RegisterUserUseCase:
    @staticmethod
    def execute(data: UserCreateDTO):
        if UserRepository.get_by_email(data.email):
            raise ValueError("User already exists")

        hashed_password = generate_password_hash(data.password)
        return UserRepository.create(data.email, hashed_password, data.role)
