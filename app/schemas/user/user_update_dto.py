from typing import Literal

from pydantic import BaseModel, constr


class UserUpdateDTO(BaseModel):
    role: Literal["user", "admin", "moderator"] = "user"
    color_theme: Literal["dark", "light"] = "dark"
    font_size: Literal["large", "medium", "small"] = "medium"
