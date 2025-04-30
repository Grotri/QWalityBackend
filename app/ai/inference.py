from io import BytesIO

import requests
from PIL import Image

from app.ai.model import yolo_model


def run_inference(image_path: str, conf_threshold: float = 0.25):
    try:
        if image_path.startswith("http"):
            # Загружаем изображение по ссылке
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
            results = yolo_model.predict(source=image, imgsz=416, conf=conf_threshold, device="cpu")
        else:
            # Предполагаем, что это локальный файл
            results = yolo_model.predict(source=image_path, imgsz=416, conf=conf_threshold, device="cpu")

        return results

    except Exception as e:
        raise RuntimeError(f"Inference error: {e}")
