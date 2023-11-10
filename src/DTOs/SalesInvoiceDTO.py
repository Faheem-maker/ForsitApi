from typing_extensions import Unpack
from pydantic import BaseModel, validator
from pydantic.config import ConfigDict
from models.Product import Product as Model
from typing import List

class Product(BaseModel):
    id: int
    qty: int
    rate: int = 0
    discount: int = 0
    tax: int = 0

    def get_rates(self):
        if self.rate == 0:
            self.rate = Model.get_by_id(self.id).price

        return self.rate
        
class SalesInvoiceDTO(BaseModel):
    products: List[Product]