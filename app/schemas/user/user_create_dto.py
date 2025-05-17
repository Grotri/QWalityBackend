from typing import Literal

from pydantic import BaseModel, EmailStr, constr


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    role: Literal["user", "admin", "moderator"] = "user"
    color_theme: str = "dark"
    font_size: str = "medium"
