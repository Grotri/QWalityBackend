from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User
from app.schemas.sub_user_create_dto import SubUserCreateDTO
from app.utils.auth import get_current_user


class CreateSubUserUseCase:
    @staticmethod
    def execute(data: SubUserCreateDTO):
        owner = get_current_user()

        new_user = User(
            email=data.email,
            hashed_password=generate_password_hash(data.password),
            role=data.role,
            client_id=owner.client_id,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
