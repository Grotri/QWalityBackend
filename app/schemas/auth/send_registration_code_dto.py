from pydantic import BaseModel, EmailStr


class SendRegistrationCodeDTO(BaseModel):
    email: EmailStr
