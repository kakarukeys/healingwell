""" Project settings """


# import local settings overriding the defaults
try:
    from settings_local import *
except ImportError:
    import sys
    sys.stderr.write( "local settings not available\n" )
