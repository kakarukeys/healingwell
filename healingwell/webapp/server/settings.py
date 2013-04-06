from healingwell.settings import POSTGRES

""" Flask settings """

DEBUG = False

DATABASE = POSTGRES.copy()
DATABASE["engine"] = "peewee.PostgresqlDatabase"
DATABASE["name"] = DATABASE["database"]
del DATABASE["database"]

# import local settings overriding the defaults
try:
    from settings_local import *
except ImportError:
    import sys
    sys.stderr.write( "local settings not available\n" )
