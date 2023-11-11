from pydantic import BaseModel
from typing import List
from datetime import date

class SalesFilter(BaseModel):
    product_id: int = 0
    products: List[int] = []
    frmDate: date = None
    toDate: date = None