from flask_jwt_extended import get_jwt_identity

from app.repositories.user_repository import UserRepository


def get_current_user():
    user_id = get_jwt_identity()
    return UserRepository.get_by_id(user_id)
