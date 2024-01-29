# from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import get_database_name
from models import Base


def init_db(engine):
    db_name = get_database_name()
    if not database_exists(db_name):
        create_database(db_name)

    # TODO: init schema

    Base.metadata.create_all(engine)

    # session = sessionmaker(bind=engine)
    # db_session = session()
