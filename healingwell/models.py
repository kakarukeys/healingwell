from peewee import PostgresqlDatabase, Model
from settings import POSTGRES

db = PostgresqlDatabase(**POSTGRES)

class BaseModel(Model):
    class Meta:
        database = db
