from datetime import datetime

from app.repositories.inspection_repository import InspectionRepository


def serialize_defect_with_product_and_inspection(defect):
    inspection = defect.inspection
    product = inspection.product
    camera_id = product.camera_id

    inspections = InspectionRepository.get_last_hundred_by_camera_id(camera_id=camera_id)
    if inspections:
        defect_count = sum(1 for i in inspections if i.result == "defective")
        defect_percent = round((defect_count / len(inspections)) * 100, 2)
        uptime = str(datetime.utcnow() - inspections[0].inspected_at).split(".")[0]
    else:
        defect_percent = 0
        uptime = 0

    return {
        "defect_id": defect.id,
        "inspection_id": inspection.id,
        "product_id": product.id,

        "label": defect.label,
        "confidence": round(defect.confidence, 2),
        "timestamp": inspection.inspected_at.strftime("%H:%M:%S %d.%m.%Y"),
        "download_image_url": f"{product.image_url}?download",  # ссылка с принудительным скачиванием
        "uptime": uptime,
        "defect_percent": defect_percent
    }
