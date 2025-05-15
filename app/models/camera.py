from datetime import datetime

from app.extensions import db


class Camera(db.Model):
    __tablename__ = "camera"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    camera_url = db.Column(db.String(255), nullable=True)

    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    status = db.Column(db.String(20), default="active")  # active / non-active / deleted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    client = db.relationship("Client", backref="camera")
