import os
from datetime import datetime
from unittest.mock import patch

import pytest
from freezegun import freeze_time

from database import migrate, execute_statement, get_now_timestamp
from tests.utils import ObjectsRollback

DB_NAME = 'test_timesheet.db'

FROZEN_DT = datetime(2023, 6, 11, 23, 30, 59, 123)


@pytest.fixture
def frozen_ts():
    with freeze_time(FROZEN_DT):
        local_dt = datetime.now()
        local_ts = local_dt.timestamp()
        utc_dt = datetime.utcfromtimestamp(local_ts)
        utc_ts = utc_dt.timestamp()
        frozen_ts = round(utc_ts)
        yield frozen_ts


@pytest.fixture(scope='session')
def db():
    try:
        if os.path.exists(DB_NAME):
            os.unlink(DB_NAME)

        with patch('database.get_database_name', return_value=DB_NAME):
            print(f'Init test database: {DB_NAME}')
            migrate()
            yield
    finally:
        print(f'Drop test database: {DB_NAME}')
        os.unlink(DB_NAME)


@pytest.fixture
def category():
    """Make one category"""
    try:
        category_id = execute_statement(
            'INSERT INTO main.categories (name, description) VALUES (?, ?)',
            'CategoryName',
            'CategoryDescription',
        )
        yield category_id
    finally:
        execute_statement('DELETE FROM main.categories WHERE id=?', category_id)


@pytest.fixture
def categories(request):
    assert isinstance(request.param, int) and request.param > 0, \
        'Incorrect parametrization for the fixture "categories".'

    ids = []

    try:
        for i in range(request.param):
            category_id = execute_statement(
                'INSERT INTO main.categories (name, description) VALUES (?, ?)',
                f'CategoryName#{i}',
                f'CategoryDescription#{i}',
            )
            ids.append(category_id)

        yield ids
    finally:
        for category_id in ids:
            execute_statement('DELETE FROM main.categories WHERE id=?', category_id)


@pytest.fixture
def task(category):
    """Make one task"""
    category_id = category
    task_id = None
    try:
        task_id = execute_statement(
            'INSERT INTO main.tasks (name, category_id) VALUES (?, ?)',
            'TaskName',
            category_id,
        )
        yield task_id, category_id
    finally:
        execute_statement('DELETE FROM main.tasks WHERE id=?', task_id)


@pytest.fixture
def tasks(request, category):
    assert isinstance(request.param, int) and request.param > 0, \
        'Incorrect parametrization for the fixture "tasks".'

    category_id = category
    ids = []

    try:
        for i in range(request.param):
            task_id = execute_statement(
                'INSERT INTO main.tasks (name, category_id) VALUES (?, ?)',
                f'TaskName#{i}',
                category_id,
            )
            ids.append((task_id, category_id))

        yield ids
    finally:
        for task_id, _ in ids:
            execute_statement('DELETE FROM main.tasks WHERE id=?', task_id)


@pytest.fixture
def work_item(task):
    task_id, _ = task
    work_item_id = None
    ts = get_now_timestamp()
    try:
        work_item_id = execute_statement(
            'INSERT INTO main.work_items (task_id, start_timestamp) VALUES (?, ?)',
            task_id,
            ts,
        )

        yield work_item_id, task_id
    finally:
        execute_statement('DELETE FROM main.work_items WHERE id=?', work_item_id)


@pytest.fixture
def objects_rollback():
    with ObjectsRollback() as roll:
        yield roll
