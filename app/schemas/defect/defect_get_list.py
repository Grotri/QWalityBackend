from pydantic import BaseModel


# Срань, вроде не понадобится
class DefectGetListaDTO(BaseModel):
    product_id: int
    min_conf = float
    max_conf = float
    date_from = str  # В теории, на дату нужно перевести
    date_to = str  # В теории, на дату нужно перевести
