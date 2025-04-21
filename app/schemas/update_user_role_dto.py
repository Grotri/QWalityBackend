from typing import Literal

from pydantic import BaseModel


class UpdateUserRoleDTO(BaseModel):
    role: Literal["user", "moderator", "admin"] # Owner тут нет потому что его нельзя назначить запросом
