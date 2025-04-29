from app.extensions import db


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    tin = db.Column(db.String(20), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # legal person / individual
    conf_threshold = db.Column(db.Float, default=0.25)

    # Relationships (опционально)
    users = db.relationship("User", backref="client", lazy=True)
    payments = db.relationship("Payment", backref="client", lazy=True)
    licenses = db.relationship("License", backref="client", lazy=True)
