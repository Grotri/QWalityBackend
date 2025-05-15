from app.models.defect import Defect
from app.models.inspection import Inspection
from app.repositories.inspection_repository import InspectionRepository
from app.utils.auth import get_current_user


class GetAnalyticsSummaryUseCase:
    @staticmethod
    def execute():
        user = get_current_user()
        client_id = user.client_id

        # total_inspections = (
        #     Inspection.query
        #     .join(Inspection.product)
        #     .filter(Inspection.product.has(client_id=client_id))
        #     .count()
        # )
        total_inspections = (
            InspectionRepository.get_all_by_client(client_id=client_id)
        )

        defective_count = (
            Inspection.query
            .join(Inspection.product)
            .filter(Inspection.product.has(client_id=client_id))
            .filter(Inspection.result == "defective")
            .count()
        )

        total_defects = (
            Defect.query
            .join(Defect.inspection)
            .join(Inspection.product)
            .filter(Inspection.product.has(client_id=client_id))
            .count()
        )

        return {
            "inspections_total": total_inspections,
            "defective_inspections": defective_count,
            "defect_percentage": round((defective_count / total_inspections) * 100, 2) if total_inspections else 0,
            "defects_total": total_defects
        }
