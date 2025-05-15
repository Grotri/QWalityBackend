from app.ai.inference import run_inference
from app.repositories.defect_repository import DefectRepository
from app.repositories.inspection_repository import InspectionRepository
from app.repositories.product_repository import ProductRepository
from app.services.minio_client import MinioClient
from app.utils.auth import get_current_client


class InspectProductUseCase:
    @staticmethod
    def execute(batch_number: str, camera_id: int, image):
        minio = MinioClient()
        image_url = minio.upload_file(image.stream, image.filename)

        product = ProductRepository.create(
            batch_number=batch_number,
            camera_id=camera_id
        )

        # запуск inference
        ai_result = run_inference(image_url)
        result = "defective" if ai_result.defects else "intact"

        inspection = InspectionRepository.create(
            product_id=product.id,
            client_id=get_current_client(),
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
