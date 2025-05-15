from typing import Literal

from pydantic import BaseModel, EmailStr, constr, Field


class SubUserCreateDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    role: Literal["user", "admin", "moderator"] = "user"
    color_theme: str = "light"
    font_size: int = Field(default=14, ge=10, le=30)
