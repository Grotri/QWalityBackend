from app.models import Payment
from app.extensions import db
from datetime import datetime
from typing import Dict, Any


class PaymentRepository:
    @staticmethod
    def get_by_id(payment_id: int) -> Payment | None:
        return Payment.query.get(payment_id)

    @staticmethod
    def get_by_payment_uid(payment_uid: str) -> Payment | None:
        return Payment.query.filter_by(payment_id=payment_uid).first()

    @staticmethod
    def get_all_by_client(client_id: int) -> list[Payment]:
        return Payment.query.filter_by(client_id=client_id).all()

    @staticmethod
    def get_created_by_client_id(client_id: int):
        return Payment.query.filter_by(client_id=client_id, status="created").first()

    @staticmethod
    def create(
            client_id: int,
            tariff_id: int,
            payment_uid: str,
            amount: int,
            status: str = "created"
    ) -> Payment:
        payment = Payment(
            client_id=client_id,
            tariff_id=tariff_id,
            payment_id=payment_uid,
            amount=amount,
            status=status
        )
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def update_status(payment_id: int, status: str, confirmed_at: datetime | None = None) -> Payment:
        payment = PaymentRepository.get_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        payment.status = status
        if confirmed_at:
            payment.confirmed_at = confirmed_at

        db.session.commit()
        return payment

    @staticmethod
    def update_payment_data(payment_id: int, data: Dict[str, Any]) -> Payment:
        """
        Обновляет данные платежа
        :param payment_id: ID платежа
        :param data: Словарь с данными для обновления
        :return: Обновленный платеж
        """
        payment = PaymentRepository.get_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")
            
        # Обновляем все переданные поля
        for key, value in data.items():
            if hasattr(payment, key):
                setattr(payment, key, value)
        
        db.session.commit()
        return payment

    @staticmethod
    def delete(payment_id: int):
        payment = PaymentRepository.get_by_id(payment_id)
        if payment:
            db.session.delete(payment)
            db.session.commit()
