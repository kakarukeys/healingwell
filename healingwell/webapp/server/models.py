from flask_peewee.db import Database
from healingwell.webapp.server.app import app

db = Database(app)
