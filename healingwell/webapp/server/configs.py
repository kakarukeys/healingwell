from healingwell.settings import POSTGRES

""" Flask configs """

DEBUG = False

DATABASE = POSTGRES.copy()
DATABASE["engine"] = "peewee.PostgresqlDatabase"
DATABASE["name"] = DATABASE["database"]
del DATABASE["database"]

# import local configs overriding the defaults
try:
    from configs_local import *
except ImportError:
    import sys
    sys.stderr.write( "local configs not available\n" )
