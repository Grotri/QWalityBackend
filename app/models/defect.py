from app.extensions import db


class Defect(db.Model):
    __tablename__ = "defect"

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey("inspection.id"), nullable=False)

    label = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)

    inspection = db.relationship("Inspection", backref="defects")
