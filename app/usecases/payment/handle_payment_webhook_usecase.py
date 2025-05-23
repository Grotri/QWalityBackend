import os
from datetime import datetime

from app.repositories.client_repository import ClientRepository
from app.repositories.license_repository import LicenseRepository
from app.repositories.payment_repository import PaymentRepository
from app.utils.freekassa_validator import FreekassaValidator
from app.utils.freekassa_exceptions import FreekassaWebhookError


class HandlePaymentWebhookUseCase:
    @staticmethod
    def execute(merchant_id: str, amount: str, order_id: str, sign: str, ip: str = None):
        """
        Обрабатывает webhook от FreeKassa
        :param merchant_id: ID магазина
        :param amount: Сумма платежа
        :param order_id: ID заказа
        :param sign: Подпись для проверки запроса
        :param ip: IP-адрес, с которого пришел запрос (опционально)
        :return: True в случае успешной обработки
        """
        # Создаем данные для валидации
        webhook_data = {
            "MERCHANT_ID": merchant_id,
            "AMOUNT": amount,
            "MERCHANT_ORDER_ID": order_id,
            "SIGN": sign
        }
        
        # Проверяем подпись и другие параметры вебхука
        secret_word2 = os.getenv("FREEKASSA_SECRET_WORD2")
        FreekassaValidator.validate_webhook(
            data=webhook_data,
            merchant_id=merchant_id,
            secret_key2=secret_word2,
            client_ip=ip
        )
        
        # Получаем ID платежа из параметра order_id
        try:
            payment_id = int(order_id)
        except ValueError:
            raise FreekassaWebhookError(f"Некорректный ID заказа: {order_id}")
        
        # Получаем платеж из БД
        payment = PaymentRepository.get_by_id(payment_id)
        if not payment:
            raise FreekassaWebhookError(f"Платеж с ID {payment_id} не найден")
        
        if payment.status != "created":
            # Если платеж уже обработан, то просто возвращаем успех
            # без выполнения дополнительных действий
            return True

        # Получаем клиента
        client = ClientRepository.get_by_id(payment.client_id)
        if not client:
            raise FreekassaWebhookError(f"Клиент с ID {payment.client_id} не найден")

        # Обновляем данные платежа
        payment_data = {
            "status": "paid",
            "confirmed_at": datetime.utcnow(),
            "payment_metadata": webhook_data
        }
        
        # Обновляем платеж с новыми данными
        PaymentRepository.update_payment_data(
            payment_id=payment.id,
            data=payment_data
        )

        # Активируем лицензию на 30 дней
        LicenseRepository.create(
            client_id=client.id,
            tariff_id=payment.tariff_id,
            payment_id=payment.id,
            status="active",
            expired_at=datetime.utcnow().replace(day=datetime.utcnow().day + 30)
        )
        
        return True
