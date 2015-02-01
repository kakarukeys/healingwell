# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Post(Item):
    page_url = Field()

    post_url = Field()
    post_author = Field()
    post_author_url = Field()
    post_author_rank = Field()
    post_date = Field()
    post_content = Field()

    thread_url = Field()
    thread_title = Field()

    section_url = Field()
    section_title = Field()
