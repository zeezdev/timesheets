from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from api import app
from dt import dt_to_ts
from tests.const import LOCAL_TZ, FROZEN_LOCAL_DT
from tests.factories import CategoryFactory, TaskFactory, WorkItemFactory

client = TestClient(app)


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
