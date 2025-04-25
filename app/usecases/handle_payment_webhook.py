from datetime import datetime

from app.extensions import db
from app.models.license import License
from app.models.payment import Payment


class HandlePaymentWebhookUseCase:
    @staticmethod
    def execute(payment_id: str, status: str):
        payment = Payment.query.filter_by(payment_id=payment_id).first()
        if not payment:
            raise ValueError("Payment not found")

        if payment.status == "paid":
            return  # Уже обработан

        if status == "succeeded":
            payment.status = "paid"
            payment.confirmed_at = datetime.utcnow()

            # Активируем лицензию на 30 дней (можно вынести в Tariff)
            license = License(
                client_id=payment.client_id,
                tariff_id=payment.tariff_id,
                payment_id=payment.id,
                status="active",
                activated_at=datetime.utcnow(),
                expired_at=datetime.utcnow().replace(day=datetime.utcnow().day + 30)
            )
            db.session.add(license)
        else:
            payment.status = "failed"

        db.session.commit()
