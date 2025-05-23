from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")

    color_theme = db.Column(db.String(20), nullable=False, default="dark")
    font_size = db.Column(db.String(20), nullable=False, default="medium")

    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
