import hashlib
import os
from datetime import datetime

from app.extensions import db
from app.models.client import Client
from app.models.license import License
from app.models.payment import Payment


class HandlePaymentWebhookUseCase:
    @staticmethod
    def execute(merchant_id: str, amount: str, order_id: str, sign: str):
        secret_word2 = os.getenv("FREEKASSA_SECRET_WORD2")

        # Проверка подписи
        check_string = f"{merchant_id}:{amount}:{secret_word2}:{order_id}"
        expected_sign = hashlib.md5(check_string.encode("utf-8")).hexdigest()
        if sign.lower() != expected_sign.lower():
            raise ValueError("Invalid signature")

        client_id = int(order_id)
        client = Client.query.get(client_id)
        if not client:
            raise ValueError("Client not found")

        payment = Payment.query.filter_by(client_id=client.id, status="created").first()
        if not payment:
            raise ValueError("Payment not found or already processed")

        # Подтверждаем платёж
        payment.status = "paid"
        payment.confirmed_at = datetime.utcnow()
        db.session.commit()

        # Активируем лицензию на 30 дней
        license = License(
            client_id=client.id,
            tariff_id=payment.tariff_id,
            payment_id=payment.id,
            status="active",
            activated_at=datetime.utcnow(),
            expired_at=datetime.utcnow().replace(day=datetime.utcnow().day + 30)
        )
        db.session.add(license)
        db.session.commit()
