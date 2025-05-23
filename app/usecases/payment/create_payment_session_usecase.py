import uuid
from app.repositories.payment_repository import PaymentRepository
from app.repositories.tariff_repository import TariffRepository
from app.services.freekassa_client import FreeKassaClient
from app.utils.auth import get_current_user


class CreatePaymentSessionUseCase:
    @staticmethod
    def execute(tariff_id: int):
        user = get_current_user()
        if user.role != "owner":
            raise PermissionError("Only owner can initiate payments.")

        tariff = TariffRepository.get_by_id(tariff_id=tariff_id)
        if not tariff:
            raise ValueError("Tariff not found.")

        # Генерируем уникальный ID для платежа
        payment_uid = str(uuid.uuid4())
        
        # Создаем запись о платеже в БД
        payment = PaymentRepository.create(
            client_id=user.client_id,
            tariff_id=tariff.id,
            payment_uid=payment_uid,
            amount=tariff.price
        )

        # Создаем ссылку на оплату
        client = FreeKassaClient()
        payment_url = client.create_payment_url(
            amount=tariff.price,
            order_id=payment.id,  # используем ID платежа из БД вместо client_id
            description=f"Оплата тарифа {tariff.name}"
        )

        return {
            "payment_url": payment_url,
            "payment_id": payment.id,
            "amount": tariff.price
        }
