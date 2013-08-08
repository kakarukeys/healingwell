from peewee import PostgresqlDatabase, Model
from healingwell.settings import POSTGRES

db = PostgresqlDatabase(**POSTGRES)

class BaseModel(Model):
    class Meta:
        database = db
