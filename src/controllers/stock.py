from fastapi import APIRouter
from models.Product import Product
from models.orders_products import OrdersProducts
from models.Orders import Orders
from peewee import fn, Case
from datetime import date, timedelta

router = APIRouter()

@router.get('/')
async def get_stock():
    return {
        'success': True,
        'products': [p.__data__ for p in Product.select(Product.id, Product.name, Product.qty)]
    }

@router.get('/low')
async def get_low_stock(minimum_qty: int = -1):
    return {
        'success': True,
        'products': [p.__data__ for p in Product.select(Product.id, Product.name, Product.qty).where(Product.qty<(Product.minimum_qty if minimum_qty < 0 else minimum_qty))]
    }

@router.get('/report')
async def get_stock_report(frmDate: date, toDate: date = date.today() + timedelta(days=1)):
    query = (OrdersProducts
         .select(
             OrdersProducts.id,
             OrdersProducts.order_id,
             OrdersProducts.product_id,
             OrdersProducts.total_amount,
             Product.id,
             Product.name,
             fn.SUM(OrdersProducts.product_qty*Case(None, [((Orders.doctype == 'SI'), -1)], 1)).over(order_by=[OrdersProducts.id]).alias('qty'),
             Orders.created_at
         )
         .join(Product)
         .join(Orders, on=Orders.id==OrdersProducts.order_id)
         .where(
             (Orders.created_at.between(frmDate, toDate))
         )
         .order_by(Orders.created_at))
    
    return {
        'success': True,
        'data': [{
            'transaction_date': p.__rel__['product_id'].orders.__data__['created_at'],
            'product_id': p.__rel__['product_id'].__data__['id'],
            'product_name': p.__rel__['product_id'].__data__['name'],
            'qty_in': p.qty if p.qty > 0 else 0,
            'qty_out': p.qty * -1 if p.qty < 0 else 0,
        } for p in query]
    }