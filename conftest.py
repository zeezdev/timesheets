import os
from unittest.mock import patch

import pytest

from database import migrate, execute_statement
from tests.utils import ObjectsRollback

DB_NAME = 'test_timesheet.db'


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
def objects_rollback():
    with ObjectsRollback() as roll:
        yield roll
