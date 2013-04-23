from flask_peewee.auth import Auth
from healingwell.webapp.server.app import app
from healingwell.webapp.server.models import db

auth = Auth(app, db)
User = auth.User
