from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import get_database_name
from models import Base

engine = create_engine(
    get_database_name(),
    echo=True,
    # This is to prevent accidentally sharing the same connection
    # for different things (for different requests).
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine
    connect_args={'check_same_thread': False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session_context = {}


def init_db():
    db_name = get_database_name()
    if not database_exists(db_name):
        create_database(db_name)

    # TODO: init schema

    Base.metadata.create_all(engine)


def get_db():
    """TODO: Docstring"""
    db_session = db_session_context.get('session')
    if db_session:
        yield db_session
        return

    try:
        db_session = SessionLocal()
        yield db_session
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise
    finally:
        db_session.close()
        db_session_context.pop('session', None)
