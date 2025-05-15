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

        client = FreeKassaClient()
        payment_url = client.create_payment_url(
            amount=tariff.price,
            order_id=user.client_id,  # например, client_id используем как ID заказа
            description=f"Оплата тарифа {tariff.name}"
        )

        payment = PaymentRepository.create(
            client_id=user.client_id,
            tariff_id=tariff.id,
            payment_uid="check line 30 in create_payment_session.py",  # todo: Это ошибка-затычка, так быть не должно
            amount=tariff.price
        )

        return {
            "payment_url": payment_url,
            "amount": tariff.price
        }
