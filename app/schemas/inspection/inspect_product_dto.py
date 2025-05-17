from pydantic import BaseModel, constr, ConfigDict
from werkzeug.datastructures import FileStorage


class InspectProductDTO(BaseModel):
    camera_url: str
    batch_number: constr(min_length=1)
    camera_id: int
    image: FileStorage

    model_config = ConfigDict(arbitrary_types_allowed=True)
