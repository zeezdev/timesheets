import time

import pytest
from unittest.mock import patch

from sqlalchemy_utils import database_exists, drop_database

from config import get_database_name
from database import engine, SessionLocal
from dt import get_local_tz
from manage import init_db
from tests.const import FROZEN_LOCAL_DT

from database import db_session_context


@pytest.fixture
def frozen_ts():
    """Mock `dt.get_now_timestamp` with a return value == FROZEN_LOCAL_DT."""
    dt_without_tz = FROZEN_LOCAL_DT.replace(tzinfo=None)
    dt_with_tz = FROZEN_LOCAL_DT.replace(tzinfo=get_local_tz())
    utc_dt = dt_without_tz - dt_with_tz.utcoffset()
    timestamp = time.mktime(utc_dt.timetuple())
    # TODO: utctimetuple ?
    ts = int(timestamp)

    with patch(
        'dt.get_now_timestamp', return_value=ts,
    ), patch(
        'tests.factories.get_now_timestamp', return_value=ts,
    ), patch(
        'services.get_now_timestamp', return_value=ts,
    ):
        yield ts


@pytest.fixture(scope='session')
def db():
    db_name = get_database_name()

    if database_exists(db_name):
        drop_database(db_name)

    init_db(engine)
    # Session.configure(bind=engine)
    yield
    drop_database(db_name)


@pytest.fixture(scope='function', autouse=True)
def session(db):
    # session = Session()
    session = SessionLocal()
    session.begin_nested()
    db_session_context['session'] = session
    yield session
    session.rollback()
    db_session_context.pop('session', None)
