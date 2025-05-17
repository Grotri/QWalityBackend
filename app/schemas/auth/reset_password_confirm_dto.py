from pydantic import BaseModel, EmailStr


class ResetPasswordConfirmDTO(BaseModel):
    email: EmailStr
    code: int
    new_password: str
