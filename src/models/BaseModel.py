from peewee import MySQLDatabase, Model

db = MySQLDatabase('forsit_api', user='root', password='root')

class BaseModel(Model):
    class Meta:
        database = db