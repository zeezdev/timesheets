from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_database_name

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
