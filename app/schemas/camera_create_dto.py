from pydantic import BaseModel


class CameraCreateDTO(BaseModel):
    name: str
    preview_url: str
