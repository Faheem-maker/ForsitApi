from fastapi import APIRouter, status, HTTPException
from models.Orders import Orders
from models.orders_products import OrdersProducts
from models.Product import Product
from DTOs.SalesInvoiceDTO import SalesInvoiceDTO
from datetime import datetime, date, timedelta
from peewee import JOIN, fn
from DTOs.sales_filter import SalesFilter

router = APIRouter()

@router.get('/')
async def get_sales_invoices(filter: SalesFilter):
    products = filter.product_id.split(',')

    categories = filter.category_id.split(',')

    query = OrdersProducts.select(
        OrdersProducts.product_id,
        OrdersProducts.product_qty,
        OrdersProducts.total_amount,
        Orders.created_at
    ).join(Orders, JOIN.LEFT_OUTER).join(Product, JOIN.LEFT_OUTER, on=(Product.id == OrdersProducts.product_id)).where(Orders.doctype=='SI')

    frmDate = filter.frmDate
    toDate = filter.toDate

    if filter.period != None:
        toDate = datetime.today()
        if filter.period == 'today':
            frmDate = datetime.today()
        elif filter.period == 'week':
            day = datetime.today()
            frmDate = day - timedelta(days=day.weekday())
        elif filter.period == 'month':
            frmDate = datetime.today().replace(day=1)
        elif filter.period == 'year':
            frmDate = datetime.today().replace(month=1, day=1)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please specify a valid time period')

    if frmDate != None:
        query = query.where(Orders.created_at.between(frmDate, toDate))
    
    if len(products) > 0 and products[0] != '':
        query = query.where(OrdersProducts.product_id.in_(products))

    if len(categories) > 0 and categories[0] != '':
        query = query.where(Product.category_id.in_(categories))

    return {
        "success": True,
        "orders": [{
            "product": p.__data__['product_id'],
            "qty": p.__data__['product_qty'],
            "total": p.__data__['total_amount'],
            "created": p.__rel__['order_id'].__data__['created_at']
        } for p in query]
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

    # Update product stock
    for product in invoice.products:
        Product.update(qty=Product.qty-product.qty).where(Product.id==product.id).execute()

    return {
        "success": True,
        "id": o.id
    }