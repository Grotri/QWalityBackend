from datetime import datetime

from app.extensions import db


class Inspection(db.Model):
    __tablename__ = "inspection"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    result = db.Column(db.String(20), nullable=False)  # "intact" / "defective"
    inspected_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", backref="inspections")
    user = db.relationship("User", backref="inspections")
