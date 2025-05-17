from PIL.Image import Image

from app.ai.model import yolo_model


def run_inference(image: Image, conf_threshold: float = 0.25):
    results = yolo_model.predict(source=image, conf=conf_threshold, imgsz=416, device="cpu", verbose=False)
    detections = []

    if not results:
        return AIResult(defects=[])

    result = results[0]  # одна картинка

    for box in result.boxes:
        cls_id = int(box.cls[0].item())  # индекс класса
        label = yolo_model.names[cls_id]  # имя класса
        conf = float(box.conf[0].item())

        x1, y1, x2, y2 = box.xyxy[0].tolist()
        width = x2 - x1
        height = y2 - y1

        detections.append({
            "label": label,
            "confidence": conf,
            "bbox": [x1, y1, width, height]
        })

    return AIResult(defects=detections)


class AIResult:
    def __init__(self, defects: list[dict]):
        self.defects = defects
