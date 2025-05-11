from app.models import Inspection
from app.extensions import db


class InspectionRepository:
    @staticmethod
    def create(product_id: int, user_id: int, result: str) -> Inspection:
        inspection = Inspection(
            product_id=product_id,
            user_id=user_id,
            result=result
        )
        db.session.add(inspection)
        db.session.commit()
        return inspection
