from typing import Literal

from pydantic import BaseModel, constr


class UserCreateDTO(BaseModel):
    login: str
    password: constr(min_length=6)
    role: Literal["user", "admin", "moderator"] = "user"
    color_theme: str = "dark"
    font_size: str = "medium"
