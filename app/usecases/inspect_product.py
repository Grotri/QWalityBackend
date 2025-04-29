from datetime import datetime

from app.models.defect import Defect
from app.models.inspection import Inspection

from app.ai.inference import run_inference
from app.extensions import db
from app.utils.auth import get_current_user


class InspectProductUseCase:
    @staticmethod
    def execute(product_id: int, image_path: str, conf_threshold: float = 0.25):
        user = get_current_user()

        # TODO: validate access rights for product_id

        results = run_inference(image_path=image_path, conf_threshold=conf_threshold)

        boxes = results[0].boxes  # предсказания первого изображения

        is_defective = len(boxes) > 0

        inspection = Inspection(
            product_id=product_id,
            user_id=user.id,
            result="defective" if is_defective else "intact",
            inspected_at=datetime.utcnow()
        )
        db.session.add(inspection)
        db.session.flush()

        if is_defective:
            for box in boxes:
                defect = Defect(
                    inspection_id=inspection.id,
                    label=box.cls.item(),
                    confidence=float(box.conf.item()),
                    x=float(box.xywh[0][0]),
                    y=float(box.xywh[0][1]),
                    width=float(box.xywh[0][2]),
                    height=float(box.xywh[0][3])
                )
                db.session.add(defect)

        db.session.commit()
        return inspection
