from peewee import *

from healingwell.models import BaseModel
from healingwell.crawler.models import GERD

class NERTrainingData(BaseModel):
    gerd = ForeignKeyField(GERD, primary_key=True)
    conllstr = TextField()
    