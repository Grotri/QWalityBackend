from datetime import datetime

from app.ai.inference import run_inference
from app.extensions import db
from app.models.defect import Defect
from app.models.inspection import Inspection
from app.models.product import Product
from app.utils.auth import get_current_user


class InspectProductUseCase:
    @staticmethod
    def execute(product_id: int, image_path: str):
        user = get_current_user()

        product = Product.query.filter_by(id=product_id, camera_id=user.client.camera_id).first()
        if not product:
            raise ValueError("Product not found or unauthorized")

        conf = user.client.conf_threshold or 0.25
        results = run_inference(image_path=image_path, conf_threshold=conf)
        boxes = results[0].boxes

        is_defective = len(boxes) > 0

        inspection = Inspection(
            product_id=product.id,
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
                    label=str(box.cls.item()),
                    confidence=float(box.conf.item()),
                    x=float(box.xywh[0][0]),
                    y=float(box.xywh[0][1]),
                    width=float(box.xywh[0][2]),
                    height=float(box.xywh[0][3])
                )
                db.session.add(defect)

        db.session.commit()
        return inspection
