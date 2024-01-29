from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_database_name

engine = create_engine(
    get_database_name(),
    echo=True,
    # dialect='sqlite',
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session_context = {}


def transactional(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session = db_session_context.get('session')
        if db_session:
            # One transactional function inside another transactional one
            return func(*args, **kwargs, db_session=db_session)
        # db_session = sessionmaker()
        db_session = SessionLocal()
        db_session_context['session'] = db_session

        try:
            result = func(*args, **kwargs, db_session=db_session)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise
        finally:
            db_session.close()
            db_session_context.pop('session', None)
        return result
    return wrap_func
