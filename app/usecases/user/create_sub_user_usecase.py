from werkzeug.security import generate_password_hash

from app.repositories.user_repository import UserRepository
from app.schemas.user.user_create_dto import UserCreateDTO
from app.utils.auth import get_current_user


class CreateSubUserUseCase:
    @staticmethod
    def execute(data: UserCreateDTO):
        current_user = get_current_user()

        if not (current_user.role in ["owner", "admin"]):
            raise PermissionError("you can't create sub-users")

        new_user = UserRepository.create(
            email=data.email,
            hashed_password=generate_password_hash(data.password),
            role=data.role,
            client_id=current_user.client_id,

        )
        return new_user
