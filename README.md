healingwell
===========

Data mining with HealingWell forum posts

import nltk
nltk.download()
all

Add project path (where this README is found) to PYTHONPATH
    add2virtualenv /path/to/project/

Run this command to test crawl:
	> scraped_data.json; scrapy crawl healingwell -o scraped_data.json -t json

Run this command to crawl:
    scrapy crawl healingwell
