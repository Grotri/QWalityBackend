from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash

from app.repositories.user_repository import UserRepository
from app.schemas.user.user_login_dto import UserLoginDTO


class LoginUserUseCase:
    @staticmethod
    def execute(data: UserLoginDTO):
        user = UserRepository.get_by_email(data.email)
        if not user or not check_password_hash(user.hashed_password, data.password):
            raise ValueError("Invalid credentials")
        answer_dict = {
            "access_token": create_access_token(identity=user.id),
            "refresh_token": create_refresh_token(identity=user.id),
        }
        return answer_dict
