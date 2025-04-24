from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB


class Tariff(db.Model):
    __tablename__ = "tariff"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_limit = db.Column(db.Integer, nullable=False)
    camera_limit = db.Column(db.Integer, nullable=True)
    roles_allowed = db.Column(JSONB, nullable=False)