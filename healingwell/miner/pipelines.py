# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

import peewee as pw
from scrapy.utils.project import get_project_settings

from healingwell.database.models import db, Post


logger = logging.getLogger(__name__)

class StoragePipeline(object):
    def __init__(self):
        # connect to database
        settings = get_project_settings()
        db.init(**settings["POSTGRES"])
        db.connect()

    def process_item(self, item, spider):
        try:
            Post.create(**item)
        except pw.IntegrityError as e:
            logger.exception(e)
            logger.debug("Was trying to insert an item: {0}".format(item))

        return item
