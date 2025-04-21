from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.repositories.user_repository import UserRepository
from app.schemas.user_login_dto import UserLoginDTO


class LoginUserUseCase:
    @staticmethod
    def execute(data: UserLoginDTO):
        user = UserRepository.get_by_email(data.email)
        if not user or not check_password_hash(user.hashed_password, data.password):
            raise ValueError("Invalid credentials")
        return create_access_token(identity=user.id)
