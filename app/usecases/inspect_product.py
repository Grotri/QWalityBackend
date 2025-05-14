from flask_jwt_extended import get_jwt_identity

from app.ai.inference import run_inference
from app.repositories.defect_repository import DefectRepository
from app.repositories.inspection_repository import InspectionRepository
from app.repositories.product_repository import ProductRepository
from app.services.minio_client import MinioClient


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
            user_id=get_jwt_identity(),
            result=result
        )

        if ai_result.defects:
            defects_data = [
                {
                    "label": d["label"],
                    "confidence": d["confidence"],
                    "bbox": d["bbox"]
                }
                for d in ai_result.defects
            ]
            DefectRepository.save_many(defects_data, inspection_id=inspection.id)

        return inspection, product, ai_result, image_url
