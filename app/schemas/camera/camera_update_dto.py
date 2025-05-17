from typing import Optional, Literal

from pydantic import BaseModel


class CameraUpdateDTO(BaseModel):
    name: Optional[str] = None
    camera_url: Optional[str] = None
    status: Literal["active", "non-active", "deleted"] = None
    deleted_at: Optional[str] = None
