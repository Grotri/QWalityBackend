from app.extensions import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"), nullable=False)

    payment_id = db.Column(db.String(255), nullable=False)  # YooMoney ID
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="created")  # created, paid, failed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    # relationships
    tariff = db.relationship("Tariff", backref="payments")
