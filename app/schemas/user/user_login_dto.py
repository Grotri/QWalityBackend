from pydantic import BaseModel, EmailStr


class UserLoginDTO(BaseModel):
    login: str
    password: str
