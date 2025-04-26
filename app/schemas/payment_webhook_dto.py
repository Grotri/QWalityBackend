from pydantic import BaseModel


class PaymentWebhookDTO(BaseModel):
    MERCHANT_ID: str
    AMOUNT: str
    MERCHANT_ORDER_ID: str
    SIGN: str
