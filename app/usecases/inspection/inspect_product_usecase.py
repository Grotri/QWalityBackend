from app.ai.inference import run_inference
from app.extensions import minio
from app.repositories.defect_repository import DefectRepository
from app.repositories.inspection_repository import InspectionRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.inspection.inspect_product_dto import InspectProductDTO
from app.utils.auth import get_current_client


class InspectProductUseCase:
    @staticmethod
    def execute(dto: InspectProductDTO):
        image_url = minio.upload_file(dto.image.stream, dto.image.filename)

        product = ProductRepository.create(
            batch_number=dto.batch_number,
            camera_id=dto.camera_id,
            image_url=image_url
        )

        image = minio.download_file(image_url)

        ai_result = run_inference(image)

        result = "defective" if ai_result.defects else "intact"

        inspection = InspectionRepository.create(
            product_id=product.id,
            client_id=get_current_client().id,
            result=result
        )

        for defect in ai_result.defects:
            DefectRepository.create(
                inspection_id=inspection.id,
                label=defect["label"],
                confidence=defect["confidence"],
                x=defect["bbox"][0],
                y=defect["bbox"][1],
                width=defect["bbox"][2],
                height=defect["bbox"][3]
            )

        return inspection, product, ai_result, image_url
