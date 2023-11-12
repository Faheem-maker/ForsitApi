from peewee import PrimaryKeyField, CharField, IntegerField, DateTimeField
from .BaseModel import BaseModel

class Category(BaseModel):
    id = PrimaryKeyField()
    title = CharField(255, unique = True)