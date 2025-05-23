from app.extensions import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"), nullable=False)

    payment_id = db.Column(db.String(255), nullable=False)  # Уникальный ID платежа в нашей системе
    freekassa_id = db.Column(db.String(255), nullable=True)  # ID транзакции в системе FreeKassa
    amount = db.Column(db.Integer, nullable=False)  # Сумма в копейках
    currency = db.Column(db.String(10), default="RUB", nullable=False)  # Валюта платежа
    status = db.Column(db.String(20), nullable=False, default="created")  # created, paid, failed, canceled
    payment_method = db.Column(db.String(50), nullable=True)  # Метод оплаты (если предоставлен FreeKassa)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    
    # Дополнительные данные от FreeKassa в JSON
    payment_metadata = db.Column(db.JSON, nullable=True)

    # relationships
    tariff = db.relationship("Tariff", backref="payments")
