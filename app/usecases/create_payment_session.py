from app.extensions import db
from app.models.payment import Payment
from app.models.tariff import Tariff
from app.services.freekassa_client import FreeKassaClient
from app.utils.auth import get_current_user


class CreatePaymentSessionUseCase:
    @staticmethod
    def execute(tariff_id: int):
        user = get_current_user()
        if user.role != "owner":
            raise PermissionError("Only owner can initiate payments.")

        tariff = Tariff.query.get(tariff_id)
        if not tariff:
            raise ValueError("Tariff not found.")

        client = FreeKassaClient()
        payment_url = client.create_payment_url(
            amount=tariff.price,
            order_id=user.client_id,  # например, client_id используем как ID заказа
            description=f"Оплата тарифа {tariff.name}"
        )

        payment = Payment(
            client_id=user.client_id,
            tariff_id=tariff.id,
            amount=tariff.price,
            status="created",
            payment_id=None  # в FreeKassa мы получим ID позже в webhook-е
        )
        db.session.add(payment)
        db.session.commit()

        return {
            "payment_url": payment_url,
            "amount": tariff.price
        }
