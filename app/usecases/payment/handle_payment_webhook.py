import hashlib
import os
from datetime import datetime

from app.repositories.client_repository import ClientRepository
from app.repositories.license_repository import LicenseRepository
from app.repositories.payment_repository import PaymentRepository


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
        client = ClientRepository.get_by_id(client_id)
        if not client:
            raise ValueError("Client not found")

        payment = PaymentRepository.get_created_by_client_id(client_id)
        if not payment:
            raise ValueError("Payment not found or already processed")

        # Подтверждаем платёж
        PaymentRepository.update_status(
            payment_id=payment.id,
            status="paid",
            confirmed_at=datetime.utcnow()
        )

        # Активируем лицензию на 30 дней
        LicenseRepository.create(
            client_id=client.id,
            tariff_id=payment.tariff_id,
            payment_id=payment.id,
            status="active",
            expired_at=datetime.utcnow().replace(day=datetime.utcnow().day + 30)
        )
