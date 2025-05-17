from pydantic import BaseModel, EmailStr


class ResetPasswordRequestDTO(BaseModel):
    email: EmailStr
