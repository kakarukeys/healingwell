import psycopg2
from items import Post

POSTGRES = {
    "database": "healingwell",
    "user": "python",
    "password": "abc123",
}

class HealingwellPipeline(object):
    sql = "insert into gerd (" + \
        ','.join(Post.fields) + ") values (" + \
        ','.join("%(" + name + ")s" for name in Post.fields) + ')'

    def __init__(self):
        self.conn = psycopg2.connect(**POSTGRES)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cur.execute(self.sql, item)
        except psycopg2.Error as e:
            self.conn.rollback()
            print e
        else:
            self.conn.commit()
        return item

    def __del__(self):
        self.cur.close()
        self.conn.close()
