from peewee import MySQLDatabase, Model
from db.config import database, username, password, host

db = MySQLDatabase(database, user=username, password=password, host=host)

class BaseModel(Model):
    class Meta:
        database = db