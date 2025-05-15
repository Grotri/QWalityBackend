from werkzeug.security import generate_password_hash

from app.extensions import cache
from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.repositories.user_repository import UserRepository
from app.schemas.client.client_register_dto import ClientRegisterDTO


class RegisterClientUseCase:
    @staticmethod
    def execute(dto: ClientRegisterDTO):
        cached_code = cache.get(f"reg_code:{dto.email}")
        if not cached_code or cached_code != dto.code:
            raise ValueError("Invalid or expired verification code")

        if Client.query.filter_by(email=dto.email).first():
            raise ValueError("Client with this email already exists")
        if Client.query.filter_by(tin=dto.tin).first():
            raise ValueError("Client with this TIN already exists")

        new_client = ClientRepository.create(
            email=dto.email,
            tin=dto.tin,
            type_=dto.type,
        )

        UserRepository.create(
            email=dto.email,
            hashed_password=generate_password_hash(dto.password),
            role="owner",
            client_id=new_client.id
        )

        cache.delete(f"reg_code:{dto.email}")
