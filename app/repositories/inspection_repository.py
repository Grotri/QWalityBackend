from app.models import Inspection
from app.extensions import db


class InspectionRepository:
    @staticmethod
    def get_by_id(inspection_id: int) -> Inspection | None:
        return Inspection.query.get(inspection_id)

    @staticmethod
    def get_all_by_product(product_id: int) -> list[Inspection]:
        return Inspection.query.filter_by(product_id=product_id).all()

    @staticmethod
    def get_all_by_user(user_id: int) -> list[Inspection]:
        return Inspection.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(product_id: int, user_id: int, result: str) -> Inspection:
        inspection = Inspection(product_id=product_id, user_id=user_id, result=result)
        db.session.add(inspection)
        db.session.commit()
        return inspection

    @staticmethod
    def delete(inspection_id: int):
        inspection = InspectionRepository.get_by_id(inspection_id)
        if inspection:
            db.session.delete(inspection)
            db.session.commit()
