from app.extensions import db
from datetime import datetime


class License(db.Model):
    __tablename__ = "license"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"), nullable=True)

    activated_at = db.Column(db.DateTime, default=datetime.utcnow)
    expired_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False)  # trial, active, expired

    tariff = db.relationship("Tariff")
