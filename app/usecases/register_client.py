from werkzeug.security import generate_password_hash

from app.extensions import db, cache
from app.models.client import Client
from app.models.user import User


class RegisterClientUseCase:
    @staticmethod
    def execute(data):
        cached_code = cache.get(f"reg_code:{data.email}")
        if not cached_code or cached_code != data.code:
            raise ValueError("Invalid or expired verification code")

        if Client.query.filter_by(email=data.email).first():
            raise ValueError("Client with this email already exists")
        if Client.query.filter_by(tin=data.tin).first():
            raise ValueError("Client with this TIN already exists")

        client = Client(
            email=data.email,
            tin=data.tin,
            type=data.type
        )
        db.session.add(client)
        db.session.flush()  # Получим client.id

        owner = User(
            email=data.email,
            hashed_password=generate_password_hash(data.password),
            role="owner",
            client_id=client.id
        )
        print(owner.hashed_password)
        db.session.add(owner)
        db.session.commit()

        cache.delete(f"reg_code:{data.email}")
