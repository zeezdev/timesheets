import itertools

import pytest

from database import category_create, execute_statement, category_update, category_read, category_list, category_delete


def test_category_read(db, category):
    # Act
    result = category_read(category)

    # Assert
    result = list(result)
    assert len(result) == 2  # header + row
    assert result[1] == (category, 'CategoryName', 'CategoryDescription')


def test_category_add(db, objects_rollback):
    # Act
    category_id = category_create('test_category', 'Test Description')
    objects_rollback.add_for_rollback('main.categories', category_id)

    # Assert
    assert isinstance(category_id, int)
    result = list(execute_statement('SELECT name, description FROM main.categories WHERE id=?', category_id))
    assert len(result) == 2  # header + row
    assert result[1] == ('test_category', 'Test Description')


def test_category_update(db, category):
    # Arrange
    category_id = category

    # Act
    result = category_update(category, 'NewCategoryName', 'NewCategoryDescription')

    # Assert
    assert result is None
    result = list(execute_statement('SELECT name, description FROM main.categories WHERE id=?', category_id))
    assert len(result) == 2  # header + row
    assert result[1] == ('NewCategoryName', 'NewCategoryDescription')


@pytest.mark.parametrize('categories', [3], indirect=True)
def test_category_list(db, categories):
    # Arrange
    categories_ids = sorted(categories)

    # Act
    result = category_list()

    # Arrange
    assert isinstance(result, itertools.chain)
    result = list(result)
    assert len(result) == 4  # header + row
    expected = list(execute_statement('SELECT id, name, description FROM categories ORDER BY id'))
    assert result == expected
    assert list(map(lambda x: x[0], result[1:])) == categories_ids


def test_category_delete(db, category):
    # Arrange
    category_id = category

    # Act
    category_delete(category_id)

    # Assert
    expected = list(execute_statement('SELECT COUNT(id) FROM categories WHERE id=?', category_id))
    assert len(expected) == 2
    assert expected[1][0] == 0
