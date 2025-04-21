from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: Literal["user", "admin", "moderator", "owner"] = "user"
