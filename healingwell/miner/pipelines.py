# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import peewee as pw
from scrapy import log
from scrapy.utils.project import get_project_settings

from healingwell.database.models import db, Post


class StoragePipeline(object):
    def __init__(self):
        settings = get_project_settings()

        log.msg("Connecting to database {0}...".format(settings["POSTGRES"]["database"]))
        db.init(**settings["POSTGRES"])
        db.connect()

    def process_item(self, item, spider):
        # insert or update
        try:
            Post.create(**item)
        except pw.IntegrityError:
            record = item.copy()
            post_url = record.pop("post_url")
            log.msg("Updating record post_url={0}".format(post_url), level=log.DEBUG)
            Post.update(**record).where(Post.post_url == post_url).execute()

        return item
