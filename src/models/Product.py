from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField, ForeignKeyField
from .BaseModel import BaseModel
from .category import Category

class Product(BaseModel):
    id = PrimaryKeyField()
    name = CharField(255, unique = True)
    price = IntegerField()        # We store the price in cents
    qty = IntegerField()          # The qty should be updated for each order, it is stored to prevent recomputing everytime
    minimum_qty = IntegerField()  # Lower than this should cause an alert
    category_id = ForeignKeyField(Category, field='id', backref='products')
    created_at = DateTimeField()