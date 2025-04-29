from datetime import datetime

from app.extensions import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.String(64), nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey("camera.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    camera = db.relationship("Camera", backref="products")
