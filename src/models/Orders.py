from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField
from .BaseModel import BaseModel

class Orders(BaseModel):
    id = PrimaryKeyField()
    base_amount  = IntegerField()
    discount_amount = IntegerField()
    tax_amount = IntegerField()
    total_amount = IntegerField()
    created_at = DateTimeField()
    doctype = CharField(2)