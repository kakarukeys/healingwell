# Scrapy settings for healingwell project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'healingwell'

SPIDER_MODULES = ['healingwell.crawler.spiders']
NEWSPIDER_MODULE = 'healingwell.crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'healingwell (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
    'healingwell.crawler.pipelines.HealingwellPipeline',
]