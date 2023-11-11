from fastapi import APIRouter, status, HTTPException
from models.Product import Product
from models.Orders import Orders
from models.orders_products import OrdersProducts
from DTOs.sales_filter import SalesFilter
from DTOs.SalesInvoiceDTO import SalesInvoiceDTO
from datetime import datetime
from peewee import JOIN

router = APIRouter()

@router.get('/')
async def get_sales_invoices(filter: SalesFilter):
    query = Orders.select().join(OrdersProducts, JOIN.LEFT_OUTER).where(Orders.doctype=='SI')

    if filter.frmDate != None:
        query = query.where(Orders.created_at.between(filter.frmDate, filter.toDate))
    
    if filter.product_id:
        query = query.where(OrdersProducts.product_id==filter.product_id)
    
    if filter.products:
        query = query.where(OrdersProducts.product_id.in_(filter.products))

    return {
        "success": True,
        "orders": [p.__data__ for p in query]
    }

@router.post('/')
async def create_sales_invoice(invoice: SalesInvoiceDTO):
    if len(invoice.products) < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot create an invoice with no products",
        )
    
    # While this looks inefficient, in practice, it will not make any difference unless we have to deal with a thousand products.
    # In that case, we can optimize it. This format is more readable for a small number of products.

    base_price = sum([p.get_rates() * p.qty for p in invoice.products])

    total_tax = sum(p.tax for p in invoice.products)

    total_discount = sum(p.discount for p in invoice.products)

    o = Orders.create(base_amount=base_price, discount_amount=total_discount, tax_amount=total_tax, created_at=datetime.utcnow(), doctype="SI")

    # Create orders products
    OrdersProducts.insert_many([{
        "order_id": o.id,
        "product_id": p.id,
        "product_rate": p.rate,
        "product_qty": p.qty,
        "discount_amount": p.discount,
        "tax_amount": p.tax,
    } for p in invoice.products]).execute()

    return {
        "success": True,
        "id": o.id
    }