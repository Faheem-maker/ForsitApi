from datetime import date
from pydantic import BaseModel, validator
from models.Product import Product
from models.category import Category

class SalesFilter(BaseModel):
    frmDate: date = None
    toDate: date = date.today()
    product_id: str = ''
    category_id: int = ''
    period: str = None

    @validator("toDate", pre=True, always=True)
    def check_toDate(cls, value, values):
        frmDate = values.get("frmDate")
        if frmDate and value <= frmDate:
            raise ValueError("toDate must be greater than frmDate")
        return value

    @validator("product_id")
    def check_product_exists(cls, value):
        products = cls.product_id.split(',')

        if products[0] == '':
            return

        for value in products:
            if value:
                product = Product.get_or_none(id=value)
                if not product:
                    raise ValueError("Product does not exist")
            return value

    @validator("category_id")
    def check_category_exists(cls, value):
        categories = cls.category_id.split(',').pop(0)

        if categories[0] == '':
            return

        if value:
            category = Category.get_or_none(id=value)
            if not category:
                raise ValueError("Category does not exist")
        return value
