from app.repositories.user_repository import UserRepository
from app.schemas.update_user_role_dto import UpdateUserRoleDTO
from app.utils.auth import get_current_user

ROLE_HIERARCHY = {
    "owner": 3,
    "admin": 2,
    "moderator": 1,
    "user": 0,
}


class UpdateUserRoleUseCase:
    @staticmethod
    def execute(target_user_id: int, data: UpdateUserRoleDTO):
        acting_user = get_current_user()
        target_user = UserRepository.get_by_id(target_user_id)

        if not target_user:
            raise ValueError("User not found")

        if target_user.id == acting_user.id:
            raise PermissionError("Cannot change your own role")

        if target_user.client_id != acting_user.client_id:
            raise PermissionError("Cannot change role for user from another client")

        if ROLE_HIERARCHY[target_user.role] >= ROLE_HIERARCHY[acting_user.role]:
            raise PermissionError("Cannot change role of equal or higher user")

        if ROLE_HIERARCHY[data.role] >= ROLE_HIERARCHY[acting_user.role]:
            raise PermissionError("Cannot assign equal or higher role")

        target_user.role = data.role
        return UserRepository.save(target_user)
