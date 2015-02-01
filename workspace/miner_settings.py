# -*- coding: utf-8 -*-

# Scrapy settings for miner project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from settings import POSTGRES


BOT_NAME = 'healingwell.miner'

SPIDER_MODULES = ['healingwell.miner.spiders']
NEWSPIDER_MODULE = 'healingwell.miner.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'miner (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
    'healingwell.miner.pipelines.StoragePipeline',
]
