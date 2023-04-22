import os
import sqlite3
from unittest.mock import patch

import pytest

from database import migrate, category_add, execute_statement

DB_NAME = 'test_timesheet.db'


@pytest.fixture
def db():
    try:
        with patch('database.get_database_name', return_value=DB_NAME):
            migrate()
            yield
    finally:
        print(f'drop test database: {DB_NAME}')
        os.unlink(DB_NAME)


def test_category_add(db):
    category_add('test_category', 'Test Description')

    result = list(execute_statement('SELECT name, description FROM main.categories'))
    assert len(result) == 2
    assert result[1] == ('test_category', 'Test Description')


# def test_category_(db):
#     category_add('test_category', 'Test Description')
#
#     result = list(execute_statement('SELECT name, description FROM main.categories'))
#     assert len(result) == 2
#     assert result[1] == ('test_category', 'Test Description')
