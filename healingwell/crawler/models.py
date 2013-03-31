from peewee import *
from healingwell.models import BaseModel

class GERD(BaseModel):
	page_url = CharField(max_length=100, null=True)

	post_url = CharField(max_length=100, null=True)
	post_author = CharField(max_length=30, null=True)
	post_author_url = CharField(max_length=100, null=True)
	post_date = DateTimeField(null=True)
	post_content = TextField(null=True)

	thread_url = CharField(max_length=100, null=True)
	thread_title = CharField(max_length=150, null=True)

	section_url = CharField(max_length=100, null=True)
	section_title = CharField(max_length=50, null=True)
