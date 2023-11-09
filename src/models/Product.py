from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField
from .BaseModel import BaseModel

class Product(BaseModel):
    id = PrimaryKeyField()
    name = CharField(255, unique = True)
    price = IntegerField()  # We store the price in cents
    created_at = DateTimeField()