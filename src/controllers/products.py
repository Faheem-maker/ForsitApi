from fastapi import APIRouter
from models.Product import Product
from DTOs.create_product import CreateProductDTO
from datetime import date

router = APIRouter()

@router.get('/')
async def get_products(skip: int = 0, limit: int = 50):
    count = Product.select().count()
    q = Product.select().limit(limit).offset(skip).execute()

    return {
        "count": count,
        "products": [p.__data__ for p in q],
    }

@router.post('/')
async def create_product(request: CreateProductDTO):
    product = Product.create(name=request.name, price=request.price, created_at=date.today())

    if product:
        return {
            "success": True,
            "id": product.id
        }