from app.models import User
from app.extensions import db


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all_by_client(client_id: int) -> list[User]:
        return User.query.filter_by(client_id=client_id).all()

    @staticmethod
    def create(email: str, hashed_password: str, role: str, client_id: int) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            role=role,
            client_id=client_id
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user_id: int, **kwargs) -> User:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        allowed_fields = {"email", "hashed_password", "role", "client_id", "color_theme", "font_size"}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(user, key, value)

        db.session.commit()
        return user

    @staticmethod
    def delete(user_id: int):
        user = UserRepository.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
