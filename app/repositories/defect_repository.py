from app.extensions import db
from app.models import Defect


class DefectRepository:
    @staticmethod
    def save_many(defects_data: list[dict], inspection_id: int):
        defects = []
        for d in defects_data:
            defect = Defect(
                inspection_id=inspection_id,
                label=d["label"],
                confidence=d["confidence"],
                x=d["bbox"][0],
                y=d["bbox"][1],
                width=d["bbox"][2],
                height=d["bbox"][3]
            )
            defects.append(defect)
            db.session.add(defect)
        db.session.commit()
        return defects
