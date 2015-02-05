healingwell
===========

Data mining with HealingWell forum posts

Create a python virtual environment and install all dependencies within it:

	add2virtualenv /path/to/project_root (where this file is found)
	pip install -r requirements.txt

Create a postgres database and user, key in the database connection settings in workspace/settings.py.
Create database tables:

	cd workspace
	python create_tables.py

To test crawler, temporarily comment out pipeline names in miner_settings.ITEM_PIPELINES, then run this command:

	> scraped_data.json; scrapy crawl healingwell.com -o scraped_data.json

open the file view_scraped_data.html to check the scraped data.

Run this command to crawl:

	scrapy crawl healingwell.com
