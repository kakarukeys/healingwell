import psycopg2

from healingwell.models import db

from items import Post
from models import GERD

class HealingwellPipeline(object):
    def process_item(self, item, spider):
    	db.set_autocommit(False)
        try:
            GERD.create(**item)
        except psycopg2.Error as e:
            db.rollback()
            print e
        else:
            db.commit()
        finally:
        	db.set_autocommit(True)
        return item
