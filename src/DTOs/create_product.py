from pydantic import BaseModel

class CreateProductDTO(BaseModel):
    name: str
    price: int