from pydantic import BaseModel


class PaymentCreateDTO(BaseModel):
    tariff_id: int
