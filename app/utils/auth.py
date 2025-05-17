from flask_jwt_extended import get_jwt_identity

from app.repositories.client_repository import ClientRepository
from app.repositories.user_repository import UserRepository


def get_current_user():
    user_id = get_jwt_identity()
    return UserRepository.get_by_id(user_id)


def get_current_client():
    user_id = get_jwt_identity()
    user = UserRepository.get_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    client = ClientRepository.get_by_id(user.client_id)
    if not client:
        raise ValueError("Client not found")

    return client
