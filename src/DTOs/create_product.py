from pydantic import BaseModel

class CreateProductDTO(BaseModel):
    name: str
    price: int
    category_id: int
    minimum_qty: int