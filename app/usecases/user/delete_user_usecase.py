from app.repositories.user_repository import UserRepository
from app.utils.auth import get_current_user


class DeleteUserUseCase:
    @staticmethod
    def execute(user_id: int):
        current_user = get_current_user()
        user = UserRepository.get_by_id(user_id=user_id)
        if not user:
            raise ValueError("User not found")

        if user.role in ["owner", "admin"] and current_user.role != "owner":
            raise PermissionError("Cannot delete users with this role")

        UserRepository.delete(user_id=user_id)
