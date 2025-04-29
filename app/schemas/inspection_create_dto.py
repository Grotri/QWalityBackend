from pydantic import BaseModel


class InspectionCreateDTO(BaseModel):
    product_id: int
    image_path: str  # Временный вариант, потом будет файл
