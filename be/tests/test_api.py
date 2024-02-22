from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from api import app
from dt import ts_to_dt, dt_to_ts
from models import Category, Task
from tests.const import LOCAL_TZ, FROZEN_LOCAL_DT
from tests.factories import CategoryFactory, TaskFactory, WorkItemFactory

client = TestClient(app)


#
# Category API tests
#


def test_categories_list(session):
    # Arrange
    categories = [CategoryFactory() for _ in range(3)]

    # Act
    response = client.get('/api/categories')

    # Arrange
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': c.id,
            'name': c.name,
            'description': c.description,
        } for c in categories
    ]


def test_categories_retrieve(session):
    assert session.query(Category).count() == 0

    # Arrange
    category = CategoryFactory()

    # Act
    response = client.get(f'/api/categories/{category.id}')

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        'id': category.id,
        'name': category.name,
        'description': category.description,
    }


def test_categories_add(session):
    assert session.query(Category).count() == 0

    # Act
    response = client.post(
        '/api/categories',
        json={'name': 'TestCategory', 'description': 'Cat for test'},
    )

    # Assert
    assert response.status_code == 201
    category = session.query(Category).one_or_none()
    assert category is not None
    assert category.name == 'TestCategory'
    assert category.description == 'Cat for test'
    assert response.json() == {
        'id': category.id,
        'name': 'TestCategory',
        'description': 'Cat for test',
    }


def test_categories_save(session):
    # Arrange
    category = CategoryFactory()
    update_data = {
        'id': category.id,
        'name': f'{category.name} Updated',
        'description': 'New description',
    }

    # Act
    response = client.put(
        f'/api/categories/{category.id}',
        json=update_data,
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == update_data
    session.refresh(category)
    assert category.name == update_data['name']
    assert category.description == update_data['description']


#
# Task API tests
#

def test_tasks_list(session):
    # Arrange
    tasks = [
        TaskFactory(),
        TaskFactory(),
        TaskFactory(),
    ]
    # Make the last task the current one
    current_task = tasks[-1]
    wi = current_task.work_items[0]
    wi.end_timestamp = None
    session.flush()

    # Act
    response = client.get('/api/tasks')

    # Arrange
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': t.id,
            'name': t.name,
            'category': {
                'id': t.category.id,
                'name': t.category.name,
            },
            'is_current': bool(t.id == current_task.id),
            'is_archived': t.is_archived,
        } for t in tasks
    ]


def test_tasks_retrieve(session):
    # Arrange
    task = TaskFactory()

    # Act
    response = client.get(f'/api/tasks/{task.id}')

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        'id': task.id,
        'name': task.name,
        'category': {
            'id': task.category.id,
            'name': task.category.name,
        },
        'is_current': 0,
        'is_archived': task.is_archived,
    }


def test_tasks_add(session):
    # Arrange
    category = CategoryFactory()
    create_data = {
        'name': 'TestTask',
        'category': {
            'id': category.id,
            'name': category.name,
        },
    }

    # Act
    response = client.post(
        '/api/tasks',
        json=create_data,
    )

    # Assert
    assert response.status_code == 201
    res_json = response.json()
    task_id = res_json['id']
    assert res_json == {**create_data, 'id': task_id, 'is_current': 0, 'is_archived': False}
    created_task = session.query(Task).filter(Task.id == task_id).one_or_none()
    assert created_task.name == create_data['name']
    assert created_task.category == category
    assert created_task.is_archived is False  # new task always is not archived


def test_tasks_save(session):
    # Arrange
    task = TaskFactory(is_archived=False)
    new_category = CategoryFactory()
    update_data = {
        'id': task.id,
        'name': f'{task.name} Updated',
        'category': {
            'id': new_category.id,
            # Category.name is not required here
        },
        # 'is_current': 0,
        'is_archived': True,
    }
    expected_response = {
        **update_data,
        'is_current': 0,
        'category': {'id': new_category.id, 'name': new_category.name},
        'is_archived': True,
    }

    # Act
    response = client.put(f'/api/tasks/{task.id}', json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_response
    session.refresh(task)
    assert task.name == update_data['name']
    assert task.category == new_category
    assert task.is_archived is True


#
# Work API tests
#

def test_work_start(session, frozen_ts):
    # Arrange
    task = TaskFactory()
    expected_start_dt = ts_to_dt(frozen_ts).replace(microsecond=0).isoformat()

    # Act
    response = client.post('/api/work/start', json={'task_id': task.id})

    # Assert
    assert response.status_code == 201
    assert len(task.work_items) == 2
    wi_current = task.work_items[-1]
    assert response.json() == {
        'id': wi_current.id,
        'task_id': task.id,
        'start_dt': expected_start_dt,
        'end_dt': None,
    }


def test_work_stop_current(session, frozen_ts):
    # Arrange
    task = TaskFactory()
    wi_current = task.work_items[0]
    wi_current.end_timestamp = None
    session.flush()
    expected_end_timestamp = frozen_ts

    # Act
    response = client.post('/api/work/stop_current')

    # Assert
    assert response.status_code == 200
    assert response.json() == None
    session.refresh(wi_current)
    assert wi_current.end_timestamp == expected_end_timestamp


def test_get_work_report(session, frozen_ts):
    # Arrange
    category1 = CategoryFactory(name='CategoryName1', description='CategoryDescription1')
    category2 = CategoryFactory(name='CategoryName2', description='CategoryDescription2')
    CategoryFactory(name='CategoryName3', description='CategoryDescription3')

    task_c1_1 = TaskFactory(name='TaskName1', category=category1, work_items=[])
    task_c1_2 = TaskFactory(name='TaskName2', category=category1, work_items=[])
    task_c2_1 = TaskFactory(name='TaskName3', category=category2, work_items=[])

    start_dt_str=datetime(2023, 3, 15, tzinfo=LOCAL_TZ).isoformat()
    end_dt_str=datetime(2023, 4, 16, tzinfo=LOCAL_TZ).isoformat()

    # Work items before requested datetime range
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 2, 15).timestamp(),
        end_timestamp=datetime(2023, 2, 15, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 3, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 3, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 3, 14, 20).timestamp(),
        end_timestamp=datetime(2023, 3, 15).timestamp(),
    )  # 4 hours in the end

    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 2, 15).timestamp(),
        end_timestamp=datetime(2023, 2, 15, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 3, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 3, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 3, 14, 20).timestamp(),
        end_timestamp=datetime(2023, 3, 15).timestamp(),
    )  # 4 hours in the end

    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 2, 15).timestamp(),
        end_timestamp=datetime(2023, 2, 15, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 3, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 3, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 3, 14, 20).timestamp(),
        end_timestamp=datetime(2023, 3, 15).timestamp(),
    )  # 4 hours in the end

    # Work items inside requested datetime range
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 3, 15).timestamp(),
        end_timestamp=datetime(2023, 3, 15, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 4, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 4, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 4, 15, 20).timestamp(),
        end_timestamp=datetime(2023, 4, 16).timestamp(),
    )  # 4 hours in the end

    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 3, 15).timestamp(),
        end_timestamp=datetime(2023, 3, 15, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 4, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 4, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 4, 15, 20).timestamp(),
        end_timestamp=datetime(2023, 4, 16).timestamp(),
    )  # 4 hours in the end

    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 3, 15).timestamp(),
        end_timestamp=datetime(2023, 3, 15, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 4, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 4, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 4, 15, 20).timestamp(),
        end_timestamp=datetime(2023, 4, 16).timestamp(),
    )  # 4 hours in the end

    # Work items after requested datetime range
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 4, 16).timestamp(),
        end_timestamp=datetime(2023, 4, 16, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 5, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 5, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c1_1,
        start_timestamp=datetime(2023, 5, 15, 20).timestamp(),
        end_timestamp=datetime(2023, 5, 16).timestamp(),
    )  # 4 hours in the end

    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 4, 16).timestamp(),
        end_timestamp=datetime(2023, 4, 16, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 5, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 5, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c1_2,
        start_timestamp=datetime(2023, 5, 15, 20).timestamp(),
        end_timestamp=datetime(2023, 5, 16).timestamp(),
    )  # 4 hours in the end

    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 4, 16).timestamp(),
        end_timestamp=datetime(2023, 4, 16, 4).timestamp(),
    )  # 4 hours in the start
    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 5, 1, 10).timestamp(),
        end_timestamp=datetime(2023, 5, 1, 12).timestamp(),
    )  # 2 hours in the middle
    WorkItemFactory(
        task=task_c2_1,
        start_timestamp=datetime(2023, 5, 15, 20).timestamp(),
        end_timestamp=datetime(2023, 5, 16).timestamp(),
    )  # 4 hours in the end

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
        'category': {
            'id': category1.id,
            'name': category1.name,
        },
        'time': (10.0 * 60 * 60) + (10.0 * 60 * 60),  # task1(4 + 2 + 4) + task2(4 + 2 + 4)
    }, {
        'category': {
            'id': category2.id,
            'name': category2.name,
        },
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
        'task': {
            'id': task_c1_1.id,
            'name': task_c1_1.name,
            'category': {
                'id': category1.id,
                'name': category1.name,
            },
        },
        'time': 10.0 * 60 * 60,  # 4 + 2 + 4
    }, {
        'task': {
            'id': task_c1_2.id,
            'name': task_c1_2.name,
            'category': {
                'id': category1.id,
                'name': category1.name,
            },
        },
        'time': 10.0 * 60 * 60,  # 4 + 2 + 4
    }, {
        'task': {
            'id': task_c2_1.id,
            'name': task_c2_1.name,
            'category': {
                'id': category2.id,
                'name': category2.name,
            },
        },
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


def test_get_work_report_start_in_continuous_in_range(session, frozen_ts):
    """
    Case: work started in the range and continuous inside the range (till now).
    Expected EOW (end of work) is `now`.

    `sr` - start of the range.
    `er` - end of the range.
    `swi` - start of the work item.
    `ewi` - end of the work item (not present in this case).
    `now` - current timestamp.

    sr:______________:er
         ^.......
        swi     ^
               now
                |
         (expected EOW)
    """

    # Arrange
    category = CategoryFactory()
    task = TaskFactory(category=category, work_items=[])
    today = FROZEN_LOCAL_DT.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    work_start = dt_to_ts(FROZEN_LOCAL_DT - timedelta(hours=2))
    WorkItemFactory(task=task, start_timestamp=work_start, end_timestamp=None)  # 2 hours before the frozen now

    # Report: today - tomorrow
    start_dt_str = today.isoformat()
    end_dt_str = tomorrow.isoformat()

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
    assert response.json() == {'time': 2.0 * 60 * 60}

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
    assert response.json() == [{
        'task': {
            'id': task.id,
            'name': task.name,
            'category': {
                'id': category.id,
                'name': category.name,
            },
        },
        'time': 2.0 * 60 * 60,
    }]

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
    assert response.json() == [{
        'category': {
            'id': category.id,
            'name': category.name,
        },
        'time': 2.0 * 60 * 60,
    }]


def test_get_work_report_start_in_continuous_out_range(session, frozen_ts):
    """
    Case: work started in the report range and continuous outside the range (till now).
    Expected EOW (end of work) is `er`.

    `sr` - start of the range.
    `er` - end of the range.
    `swi` - start of the work item.
    `ewi` - end of the work item (not present in this case).
    `now` - current timestamp.

    sr:______________:er
         ^...................
        swi          |      ^
                     |     now
                     |
               (expected EOW)
    """

    # Arrange
    category = CategoryFactory()
    task = TaskFactory(category=category, work_items=[])
    yesterday = (FROZEN_LOCAL_DT - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    today = FROZEN_LOCAL_DT.replace(hour=0, minute=0, second=0, microsecond=0)
    work_start = dt_to_ts(today - timedelta(hours=4))
    WorkItemFactory(task=task, start_timestamp=work_start, end_timestamp=None)  # 4 hours before today

    # Report: yesterday - today
    start_dt_str = yesterday.isoformat()
    end_dt_str = today.isoformat()

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
    assert response.json() == {'time': 4.0 * 60 * 60}

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
    assert response.json() == [{
        'task': {
            'id': task.id,
            'name': task.name,
            'category': {
                'id': category.id,
                'name': category.name,
            },
        },
        'time': 4.0 * 60 * 60,
    }]

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
    assert response.json() == [{
        'category': {
            'id': category.id,
            'name': category.name,
        },
        'time': 4.0 * 60 * 60,
    }]


def test_get_work_report_start_in_end_out_range(session, frozen_ts):
    """
    Case: work started in the report range and ended outside the range (before now).
    Expected EOW (end of work) is `er`.

    `sr` - start of the range.
    `er` - end of the range.
    `swi` - start of the work item.
    `ewi` - end of the work item.
    `now` - current timestamp.

    sr:______________:er
         ^..................^....
        swi          |     ewi  ^
                     |         now
                     |
          (expected end of work)
    """

    # Arrange
    category = CategoryFactory()
    task = TaskFactory(category=category, work_items=[])
    yesterday = (FROZEN_LOCAL_DT - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    today = FROZEN_LOCAL_DT.replace(hour=0, minute=0, second=0, microsecond=0)
    work_start = dt_to_ts(today - timedelta(hours=4))
    work_end = dt_to_ts(today + timedelta(hours=2))
    WorkItemFactory(task=task, start_timestamp=work_start, end_timestamp=work_end)  # 6 hours

    # Report: yesterday - today
    start_dt_str = yesterday.isoformat()
    end_dt_str = today.isoformat()

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
    # We expect 4 hours in total for yesterday
    assert response.json() == {'time': 4.0 * 60 * 60}

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
    assert response.json() == [{
        'task': {
            'id': task.id,
            'name': task.name,
            'category':{
                'id': category.id,
                'name': category.name,
            },
        },
        'time': 4.0 * 60 * 60,
    }]

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
    assert response.json() == [{
        'category': {
            'id': category.id,
            'name': category.name,
        },
        'time': 4.0 * 60 * 60,
    }]


def test_get_work_report_start_out_end_in_range(session, frozen_ts):
    """
    Case: work started out the report range (before) and ended in the range.
    Expected SOW (start of work) is `sr`.
    Expected EOW (end of work) is `now`.

    `sr` - start of the range.
    `er` - end of the range.
    `swi` - start of the work item.
    `ewi` - end of the work item.
    `now` - current timestamp.

          sr:______________________:er
     ^.....|......^.........
    swi    |     ewi       ^
           |              now
           |
    (expected SOW)
    """

    # Arrange
    category = CategoryFactory()
    task = TaskFactory(category=category, work_items=[])
    today = FROZEN_LOCAL_DT.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    work_start = dt_to_ts(today - timedelta(hours=3))
    work_end = dt_to_ts(today + timedelta(hours=4))
    assert work_end < dt_to_ts(FROZEN_LOCAL_DT)
    WorkItemFactory(task=task, start_timestamp=work_start, end_timestamp=work_end)

    # Report for today
    start_dt_str = today.isoformat()
    end_dt_str = tomorrow.isoformat()

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
    # We expect 4 hours in total for yesterday
    assert response.json() == {'time': 4.0 * 60 * 60}

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
    assert response.json() == [{
        'task': {
            'id': task.id,
            'name': task.name,
            'category':{
                'id': category.id,
                'name': category.name,
            },
        },
        'time': 4.0 * 60 * 60,
    }]

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
    assert response.json() == [{
        'category': {
            'id': category.id,
            'name': category.name,
        },
        'time': 4.0 * 60 * 60,
    }]


def test_get_work_report_start_out_continuous_in_range(session, frozen_ts):
    """
    Case: work started out the report range (before) and continuous in the range.
    Expected SOW (start of work) is `sr`.
    Expected EOW (end of work) is `now`.

    `sr` - start of the range.
    `er` - end of the range.
    `swi` - start of the work item.
    `ewi` - end of the work item (not present in this case).
    `now` - current timestamp.

          sr:__________________:er
     ^.....|..............
    swi    |             ^
           |            now
           |             |
    (expected SOW) (expected EOW)
    """

    # Arrange
    category = CategoryFactory()
    task = TaskFactory(category=category, work_items=[])
    today = FROZEN_LOCAL_DT.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    work_start = dt_to_ts(today - timedelta(hours=3))
    WorkItemFactory(task=task, start_timestamp=work_start, end_timestamp=None)

    # Report for today
    start_dt_str = today.isoformat()
    end_dt_str = tomorrow.isoformat()

    # Act
    response = client.get(
        '/api/work/report_total',
        params={
            'start_datetime': start_dt_str,
            'end_datetime': end_dt_str,
        },
    )

    expected_time = (FROZEN_LOCAL_DT - today).seconds

    # Assert
    assert response.status_code == 200
    # We expect (start from today till now) in total for yesterday
    assert response.json() == {'time': expected_time}

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
    # We expect (start from today till now) in total for yesterday
    assert response.json() == [{
        'task': {
            'id': task.id,
            'name': task.name,
            'category': {
                'id': category.id,
                'name': category.name,
            },
        },
        'time': expected_time,
    }]

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
    assert response.json() == [{
        'category': {
            'id': category.id,
            'name': category.name,
        },
        'time': expected_time,
    }]


def test_get_work_report_start_out_end_out_range(session, frozen_ts):
    """
    Case: work started out the report range (before) and ended outside the range (after).
    Expected SOW (start of work) is `sr`.
    Expected EOW (end of work) is `er`.

    `sr` - start of the range.
    `er` - end of the range.
    `swi` - start of the work item.
    `ewi` - end of the work item.
    `now` - current timestamp.

          sr:______________:er
    ^......|................|.....^.......
    swi    |                |    ewi     ^
           |                |           now
     (expected SOW)   (expected EOW)
    """

    # Arrange
    category = CategoryFactory()
    task = TaskFactory(category=category, work_items=[])
    local_dt = FROZEN_LOCAL_DT - timedelta(days=1)
    today = FROZEN_LOCAL_DT.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    work_start = dt_to_ts(yesterday - timedelta(hours=3))
    work_end = dt_to_ts(today + timedelta(hours=3))
    WorkItemFactory(task=task, start_timestamp=work_start, end_timestamp=work_end)

    # Report for yesterday
    start_dt_str = yesterday.isoformat()
    end_dt_str = today.isoformat()

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
    # We expect 24 hours in total for yesterday
    assert response.json() == {'time': 24.0 * 60 * 60}

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
    assert response.json() == [{
        'task': {
            'id': task.id,
            'name': task.name,
            'category': {
                'id': category.id,
                'name': category.name,
            },
        },
        'time': 24.0 * 60 * 60,
    }]

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
    assert response.json() == [{
        'category': {
            'id': category.id,
            'name': category.name,
        },
        'time': 24.0 * 60 * 60,
    }]
