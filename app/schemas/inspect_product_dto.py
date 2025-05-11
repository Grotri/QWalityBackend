from pydantic import BaseModel, constr
from werkzeug.datastructures import FileStorage

class InspectProductDTO(BaseModel):
    batch_number: constr(min_length=1)
    camera_id: int
    image: FileStorage
