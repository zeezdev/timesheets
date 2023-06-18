from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from api import app
from database import execute_statement

client = TestClient(app)


#
# Category API tests
#

@pytest.mark.parametrize('categories', [3], indirect=True)
def test_categories_list(db, categories):
    # Arrange
    categories_ids = sorted(categories)

    # Act
    response = client.get(f'/api/categories')

    # Arrange
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': category_id,
            'name': f'CategoryName#{i}',
            'description': f'CategoryDescription#{i}',
        }
        for i, category_id in enumerate(categories_ids)
    ]


def test_categories_retrieve(db, category):
    # Arrange
    category_id = category

    # Act
    response = client.get(f'/api/categories/{category_id}')

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        'id': category_id,
        'name': 'CategoryName',
        'description': 'CategoryDescription',
    }


def test_categories_add(db, objects_rollback):
    # Act
    response = client.post(
        '/api/categories',
        json={'name': 'TestCategory', 'description': 'Cat for test'},
    )

    # Assert
    assert response.status_code == 201
    res_json = response.json()
    category_id = res_json['id']
    objects_rollback.add_for_rollback('categories', category_id)
    assert res_json == {
        'id': category_id,
        'name': 'TestCategory',
        'description': 'Cat for test',
    }
    result = list(execute_statement('SELECT name, description FROM main.categories WHERE id=?', category_id))
    assert len(result) == 2  # header + row
    assert result[1] == ('TestCategory', 'Cat for test')


def test_categories_save(db, category):
    # Arrange
    category_id = category
    update_data = {
        'id': category_id,
        'name': 'NewCategoryName',
        'description': 'NewCategoryDescription',
    }

    # Act
    response = client.put(f'/api/categories/{category_id}', json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == update_data
    # Validate in DB
    result = list(execute_statement('SELECT name, description FROM main.categories WHERE id=?', category_id))
    assert len(result) == 2  # header + row
    assert result[1] == ('NewCategoryName', 'NewCategoryDescription')


#
# Task API tests
#

@pytest.mark.parametrize('tasks', [3], indirect=True)
def test_tasks_list(db, tasks):
    # Arrange
    task_ids = sorted(tasks)

    # Act
    response = client.get('/api/tasks')

    # Arrange
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': task_id,
            'name': f'TaskName#{i}',
            'category_id': category_id,
            'is_current': 0,
        }
        for i, (task_id, category_id) in enumerate(task_ids)
    ]


def test_tasks_retrieve(db, task):
    # Arrange
    task_id, category_id = task

    # Act
    response = client.get(f'/api/tasks/{task_id}')

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        'id': task_id,
        'name': 'TaskName',
        'category_id': category_id,
        'is_current': 0,
    }


def test_tasks_add(db, category, objects_rollback):
    # Arrange
    category_id = category

    # Act
    response = client.post(
        '/api/tasks',
        json={'name': 'TestTask', 'category_id': category_id},
    )

    # Assert
    assert response.status_code == 201
    res_json = response.json()
    task_id = res_json['id']
    objects_rollback.add_for_rollback('tasks', task_id)
    assert res_json == {
        'id': task_id,
        'name': 'TestTask',
        'category_id': category_id,
        'is_current': 0,
    }
    result = list(execute_statement('SELECT name, category_id FROM main.tasks WHERE id=?', task_id))
    assert len(result) == 2  # header + row
    assert result[1] == ('TestTask', category_id)


@pytest.mark.parametrize('categories', [1], indirect=True)
def test_tasks_save(db, task, categories):
    # Arrange
    task_id, category_id = task
    new_category_id = categories[0]
    update_data = {
        'id': task_id,
        'name': 'NewTaskName',
        'category_id': new_category_id,
        'is_current': 0,
    }

    # Act
    response = client.put(f'/api/tasks/{task_id}', json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == update_data
    # Validate in DB
    result = list(execute_statement('SELECT name, category_id FROM main.tasks WHERE id=?', task_id))
    assert len(result) == 2  # header + row
    assert result[1] == ('NewTaskName', new_category_id)


#
# Work API tests
#

def test_work_start(db, frozen_ts, task, objects_rollback):
    # Arrange
    task_id, category_id = task
    result = list(execute_statement('SELECT COUNT(id) AS count FROM main.work_items WHERE task_id=?', task_id))
    assert len(result) == 2  # header + row
    assert result[1] == (0,)
    expected_start_dt = datetime.fromtimestamp(frozen_ts).strftime('%Y-%m-%dT%H:%M:%S')

    # Act
    response = client.post(f'/api/work/start', json={'task_id': task_id})

    # Assert
    assert response.status_code == 201
    res_json = response.json()
    work_item_id = res_json['id']
    objects_rollback.add_for_rollback('work_items', work_item_id)
    assert res_json == {
        'id': work_item_id,
        'task_id': task_id,
        'start_dt': expected_start_dt,
        'end_dt': None,
    }
    result = list(execute_statement(
        'SELECT id, task_id, start_timestamp, end_timestamp '
        'FROM main.work_items WHERE task_id=?',
        task_id
    ))
    assert len(result) == 2  # header + row
    assert result[1] == (work_item_id, task_id, frozen_ts, None)


def test_work_stop_current(db, frozen_ts, work_item):
    # Arrange
    work_item_id, task_id = work_item

    # Act
    response = client.post('/api/work/stop_current')

    # Assert
    assert response.status_code == 200
    assert response.json() == None
    # Validate in DB
    result = list(execute_statement(
        'SELECT task_id, start_timestamp, end_timestamp FROM main.work_items WHERE id=?',
        work_item_id
    ))
    assert len(result) == 2  # header + row
    assert result[1] == (task_id, frozen_ts, frozen_ts)
