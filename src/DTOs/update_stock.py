from pydantic import BaseModel

class UpdateStatus(BaseModel):
    product_id: int
    qty: int