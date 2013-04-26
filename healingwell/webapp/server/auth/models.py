from peewee import *

from flask_peewee.auth import Auth

from healingwell.webapp.server.app import app
from healingwell.webapp.server.models import db

auth = Auth(app, db)
User = auth.User

class Group(db.Model):
    name = CharField(max_length=20, unique=True)

class UserGroup(db.Model):
    user = ForeignKeyField(User)
    group = ForeignKeyField(Group)

    class Meta:
        indexes = (
            (("user", "group"), True),
        )

class GroupPermission(db.Model):
    group = ForeignKeyField(Group)
    permission = CharField(max_length=40)
