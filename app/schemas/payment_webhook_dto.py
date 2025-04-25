from typing import Literal

from pydantic import BaseModel


class PaymentWebhookDTO(BaseModel):
    payment_id: str
    status: Literal["succeeded", "failed"]
