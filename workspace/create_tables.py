from healingwell.database.models import db, Post
import initialize


""" Create all tables for healingwell text analytics """

initialize.init()
db.create_tables([Post])
