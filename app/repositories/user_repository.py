from app.extensions import db
from app.models.user import User


class UserRepository:
    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(email: str, hashed_password: str, role: str = "user"):
        user = User(email=email, hashed_password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def save(user):
        db.session.commit()
        return user
