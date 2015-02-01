import logging

from healingwell.database.models import db

from settings import POSTGRES, log_file_path, log_level


""" Initialization """

def init():
    # connect to database
    db.init(**POSTGRES)
    db.connect()

    # set up logging
    logging.basicConfig(
        filename=log_file_path,
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
