from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: Literal["user", "admin", "moderator", "owner"] = "user"
