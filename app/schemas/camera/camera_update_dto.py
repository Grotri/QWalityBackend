from typing import Optional

from pydantic import BaseModel


class CameraUpdateDTO(BaseModel):
    name: Optional[str] = None
    camera_url: Optional[str]= None
    status: Optional[str]= None
    deleted_at: Optional[str]= None
