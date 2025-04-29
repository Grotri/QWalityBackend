from enum import Enum

from pydantic import BaseModel, EmailStr


class ClientType(str, Enum):
    legal = "legal person"
    individual = "individual"


class ClientRegisterDTO(BaseModel):
    email: EmailStr
    password: str
    tin: str
    type: ClientType
