from sqlalchemy import desc

from app.extensions import db
from app.models import Defect, Inspection, Product


class DefectRepository:
    @staticmethod
    def get_by_id(defect_id: int) -> Defect | None:
        return Defect.query.get(defect_id)

    @staticmethod
    def get_all_by_inspection(inspection_id: int) -> list[Defect]:
        return Defect.query.filter_by(inspection_id=inspection_id).all()

    @staticmethod
    def get_all_with_inspections_and_products_by_camera_id_and_client_id(client_id: int, camera_id: int):
        return (
            Defect.query
            .join(Inspection)
            .join(Product)
            .filter(
                Inspection.client_id == client_id,
                Product.camera_id == camera_id
            )
            .order_by(desc(Inspection.inspected_at))
            .all()
        )

    @staticmethod
    def create(
            inspection_id: int,
            label: str,
            confidence: float,
            x: float,
            y: float,
            width: float,
            height: float
    ) -> Defect:
        defect = Defect(
            inspection_id=inspection_id,
            label=label,
            confidence=confidence,
            x=x,
            y=y,
            width=width,
            height=height
        )
        db.session.add(defect)
        db.session.commit()
        return defect

    @staticmethod
    def delete(defect_id: int):
        defect = DefectRepository.get_by_id(defect_id)
        if defect:
            db.session.delete(defect)
            db.session.commit()
