from app.ai.model import yolo_model


def run_inference(image_path: str, conf_threshold: float = 0.25):
    results = yolo_model.predict(source=image_path, imgsz=416, device='cpu', conf=conf_threshold)
    return results
