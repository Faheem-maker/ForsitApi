from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField, ForeignKeyField
from .BaseModel import BaseModel
from .Orders import Orders
from .Product import Product

class OrdersProducts(BaseModel):
    id = PrimaryKeyField()
    order_id = ForeignKeyField(Orders, 'id', backref='entries')
    product_id = ForeignKeyField(Product, 'id', backref='orders')
    product_rate = IntegerField()
    product_qty = IntegerField()
    base_amount  = IntegerField()
    discount_amount = IntegerField()
    tax_amount = IntegerField()
    total_amount = IntegerField()

    class Meta:
        table_name = 'orders_products'