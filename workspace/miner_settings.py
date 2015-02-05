# -*- coding: utf-8 -*-

# Scrapy settings for miner project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from settings import POSTGRES, log_file_path, log_level


BOT_NAME = 'healingwell.miner'

SPIDER_MODULES = ['healingwell.miner.spiders']
NEWSPIDER_MODULE = 'healingwell.miner.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'miner (+http://www.yourdomain.com)'

# The integer values you assign to classes in this setting determine the order they run in-
# items go through pipelines from order number low to high.
ITEM_PIPELINES = {
    'healingwell.miner.pipelines.StoragePipeline': 0,
}

LOG_FILE = log_file_path
LOG_LEVEL = log_level

# all standard output (and error) of your process will be redirected to the log
LOG_STDOUT = True
