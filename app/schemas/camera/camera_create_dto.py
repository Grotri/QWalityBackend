from pydantic import BaseModel


class CameraCreateDTO(BaseModel):
    name: str
    camera_url: str
