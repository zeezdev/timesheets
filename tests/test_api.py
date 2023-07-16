from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from api import app
from database import execute_statement, dt_to_ts, ts_to_dt
from tests.const import FROZEN_DT, LOCAL_TZ, FROZEN_TS

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
    expected_start_dt = ts_to_dt(FROZEN_TS).replace(microsecond=0).isoformat()

    # Act
    response = client.post('/api/work/start', json={'task_id': task_id})

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


def add_work_item(task_id: int, start_dt: datetime, end_dt: datetime | None) -> int:
    start_ts = dt_to_ts(start_dt)
    end_ts = end_dt and dt_to_ts(end_dt)
    work_item_id = execute_statement(
        'INSERT INTO main.work_items (task_id, start_timestamp, end_timestamp) VALUES (?, ?, ?)',
        task_id,
        start_ts,
        end_ts,
    )
    return work_item_id


def test_get_work_report(db, frozen_ts, objects_rollback):
    # Arrange
    category1_id = execute_statement(
        'INSERT INTO main.categories (name, description) VALUES (?, ?)',
        'CategoryName1',
        'CategoryDescription1',
    )
    objects_rollback.add_for_rollback('categories', category1_id)
    category2_id = execute_statement(
        'INSERT INTO main.categories (name, description) VALUES (?, ?)',
        'CategoryName2',
        'CategoryDescription2',
    )
    objects_rollback.add_for_rollback('categories', category2_id)
    category3_id = execute_statement(
        'INSERT INTO main.categories (name, description) VALUES (?, ?)',
        'CategoryName3',
        'CategoryDescription3',
    )
    objects_rollback.add_for_rollback('categories', category3_id)

    task1_c1_id = execute_statement(
        'INSERT INTO main.tasks (name, category_id) VALUES (?, ?)',
        'TaskName1',
        category1_id,
    )
    objects_rollback.add_for_rollback('tasks', task1_c1_id)
    task2_c1_id = execute_statement(
        'INSERT INTO main.tasks (name, category_id) VALUES (?, ?)',
        'TaskName2',
        category1_id,
    )
    objects_rollback.add_for_rollback('tasks', task2_c1_id)
    task3_c2_id = execute_statement(
        'INSERT INTO main.tasks (name, category_id) VALUES (?, ?)',
        'TaskName3',
        category2_id,
    )
    objects_rollback.add_for_rollback('tasks', task3_c2_id)

    start_dt_str=datetime(2023, 3, 15, tzinfo=LOCAL_TZ).isoformat()
    end_dt_str=datetime(2023, 4, 15, 23, 59, 59, 999999, tzinfo=LOCAL_TZ).isoformat()
    # Work items before requested datetime range
    wi_id = add_work_item(task1_c1_id, datetime(2023, 2, 15), datetime(2023, 2, 15, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task1_c1_id, datetime(2023, 3, 1, 10), datetime(2023, 3, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task1_c1_id, datetime(2023, 3, 14, 20), datetime(2023, 3, 15))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    wi_id = add_work_item(task2_c1_id, datetime(2023, 2, 15), datetime(2023, 2, 15, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task2_c1_id, datetime(2023, 3, 1, 10), datetime(2023, 3, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task2_c1_id, datetime(2023, 3, 14, 20), datetime(2023, 3, 15))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    wi_id = add_work_item(task3_c2_id, datetime(2023, 2, 15), datetime(2023, 2, 15, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task3_c2_id, datetime(2023, 3, 1, 10), datetime(2023, 3, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task3_c2_id, datetime(2023, 3, 14, 20), datetime(2023, 3, 15))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    # Work items inside requested datetime range
    wi_id = add_work_item(task1_c1_id, datetime(2023, 3, 15), datetime(2023, 3, 15, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task1_c1_id, datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task1_c1_id, datetime(2023, 4, 15, 20), datetime(2023, 4, 16))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    wi_id = add_work_item(task2_c1_id, datetime(2023, 3, 15), datetime(2023, 3, 15, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task2_c1_id, datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task2_c1_id, datetime(2023, 4, 15, 20), datetime(2023, 4, 16))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    wi_id = add_work_item(task3_c2_id, datetime(2023, 3, 15), datetime(2023, 3, 15, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task3_c2_id, datetime(2023, 4, 1, 10), datetime(2023, 4, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task3_c2_id, datetime(2023, 4, 15, 20), datetime(2023, 4, 16))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    # Work items after requested datetime range
    wi_id = add_work_item(task1_c1_id, datetime(2023, 4, 16), datetime(2023, 4, 16, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task1_c1_id, datetime(2023, 5, 1, 10), datetime(2023, 5, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task1_c1_id, datetime(2023, 5, 15, 20), datetime(2023, 5, 16))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    wi_id = add_work_item(task2_c1_id, datetime(2023, 4, 16), datetime(2023, 4, 16, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task2_c1_id, datetime(2023, 5, 1, 10), datetime(2023, 5, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task2_c1_id, datetime(2023, 5, 15, 20), datetime(2023, 5, 16))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    wi_id = add_work_item(task3_c2_id, datetime(2023, 4, 16), datetime(2023, 4, 16, 4))  # 4 hours in the start
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task3_c2_id, datetime(2023, 5, 1, 10), datetime(2023, 5, 1, 12))  # 2 hours in the middle
    objects_rollback.add_for_rollback('work_items', wi_id)
    wi_id = add_work_item(task3_c2_id, datetime(2023, 5, 15, 20), datetime(2023, 5, 16))  # 4 hours in the end
    objects_rollback.add_for_rollback('work_items', wi_id)

    # Act
    response = client.get(
        '/api/work/report_by_category',
        params={
            'start_datetime': start_dt_str,
            'end_datetime': end_dt_str,
        },
    )

    # Assert
    assert response.status_code == 200
    res_json = response.json()
    assert res_json == [{
        'category_id': category1_id,
        'category_name': 'CategoryName1',
        'time': (10.0 * 60 * 60) + (10.0 * 60 * 60),  # task1(4 + 2 + 4) + task2(4 + 2 + 4)
    }, {
        'category_id': category2_id,
        'category_name': 'CategoryName2',
        'time': 10.0 * 60 * 60,  # 4 + 2 + 4
    }]

    # Act
    response = client.get(
        '/api/work/report_by_task',
        params={
            'start_datetime': start_dt_str,
            'end_datetime': end_dt_str,
        },
    )

    # Assert
    assert response.status_code == 200
    res_json = response.json()
    assert res_json == [{
        'task_id': task1_c1_id,
        'task_name': 'TaskName1',
        'category_id': category1_id,
        'time': 10.0 * 60 * 60,  # 4 + 2 + 4
    }, {
        'task_id': task2_c1_id,
        'task_name': 'TaskName2',
        'category_id': category1_id,
        'time': 10.0 * 60 * 60,  # 4 + 2 + 4
    }, {
        'task_id': task3_c2_id,
        'task_name': 'TaskName3',
        'category_id': category2_id,
        'time': 10.0 * 60 * 60,  # 4 + 2 + 4
    }]

    # Act
    response = client.get(
        '/api/work/report_total',
        params={
            'start_datetime': start_dt_str,
            'end_datetime': end_dt_str,
        },
    )

    # Assert
    assert response.status_code == 200
    res_json = response.json()
    assert res_json == {
        'time': (10.0 * 60 * 60) + (10.0 * 60 * 60) + (10.0 * 60 * 60),  # task1 + task2 + task3
    }
