from datetime import datetime
from app.utils.auth import get_current_user
from app.models.payment import Payment
from app.models.tariff import Tariff
from app.extensions import db


class CreatePaymentSessionUseCase:
    @staticmethod
    def execute(tariff_id: int):
        user = get_current_user()
        if user.role != "owner":
            raise PermissionError("Only owner can initiate payments.")

        tariff = Tariff.query.get(tariff_id)
        if not tariff:
            raise ValueError("Tariff not found.")

        # Здесь эмулируем внешний платёж
        # В реальности — делаем запрос в YooMoney, получаем ссылку
        fake_payment_id = f"pay_{datetime.utcnow().timestamp()}"
        fake_payment_url = f"https://yoomoney.ru/payments/{fake_payment_id}"

        payment = Payment(
            client_id=user.client_id,
            tariff_id=tariff.id,
            amount=tariff.price,
            status="created",
            payment_id=fake_payment_id
        )
        db.session.add(payment)
        db.session.commit()

        return {
            "payment_id": payment.payment_id,
            "amount": payment.amount,
            "payment_url": fake_payment_url
        }
