import pytest
from starlette.testclient import TestClient

from api import app
from dt import ts_to_dt, get_now_timestamp
from models import WorkItem
from tests.factories import WorkItemFactory, TaskFactory

client = TestClient(app)


def test_work_items_list_empty(session):
    assert session.query(WorkItem).count() == 0

    response = client.get('/api/work/items/')

    assert response.status_code == 200
    assert response.json() == {
        'items': [],
        'page': 1,
        'pages': 0,
        'size': 50,
        'total': 0,
    }


def test_work_items_list(session):
    work_items = WorkItemFactory.create_batch(10)

    response = client.get('/api/work/items/?page=3&size=2')

    assert response.status_code == 200
    assert response.json() == {
        'items': [{
            'id': i.id,
            'task': {'id': i.task.id, 'name': i.task.name},
            'start_dt': ts_to_dt(i.start_timestamp).isoformat(),
            'end_dt': ts_to_dt(i.end_timestamp).isoformat(),
        } for i in work_items[4:6]],
        'page': 3,
        'pages': 5,
        'size': 2,
        'total': 10,
    }


def test_work_items_get(session):
    work_item = WorkItemFactory()
    WorkItemFactory()

    response = client.get(f'/api/work/items/{work_item.id}')

    assert response.status_code == 200
    assert response.json() == {
        'id': work_item.id,
        'task': {'id': work_item.task.id, 'name': work_item.task.name},
        'start_dt': ts_to_dt(work_item.start_timestamp).isoformat(),
        'end_dt': ts_to_dt(work_item.end_timestamp).isoformat(),
    }


def test_work_items_delete(session):
    work_item = WorkItemFactory()

    response = client.delete(f'/api/work/items/{work_item.id}')

    assert response.status_code == 204
    assert session.query(WorkItem).filter(WorkItem.id == work_item.id).one_or_none() is None


def test_work_items_update(session):
    work_item = WorkItemFactory()
    new_start = work_item.start_timestamp + 10
    new_end = work_item.end_timestamp - 10
    new_task = TaskFactory()
    update_data = {
        'id': work_item.id,
        'task': {'id': new_task.id, 'name': new_task.name},
        'start_dt': ts_to_dt(new_start).isoformat(),
        'end_dt': ts_to_dt(new_end).isoformat(),
    }

    response = client.put(f'/api/work/items/{work_item.id}', json=update_data)

    assert response.status_code == 200
    assert response.json() == update_data
    session.refresh(work_item)
    assert work_item.start_timestamp == new_start
    assert work_item.end_timestamp == new_end
    assert work_item.task == new_task


def test_work_items_update_partial(session):
    """Partial update of the work item with a new task only"""
    work_item = WorkItemFactory()
    old_start = work_item.start_timestamp
    old_end = work_item.end_timestamp
    new_task = TaskFactory()
    update_data = {
        'task': {'id': new_task.id, 'name': new_task.name},
    }

    response = client.patch(f'/api/work/items/{work_item.id}', json=update_data)

    assert response.status_code == 200
    assert response.json() == {
        'id': work_item.id,
        'start_dt': ts_to_dt(old_start).isoformat(),
        'end_dt': ts_to_dt(old_end).isoformat(),
        **update_data,
    }
    session.refresh(work_item)
    assert work_item.start_timestamp == old_start
    assert work_item.end_timestamp == old_end
    assert work_item.task == new_task


@pytest.mark.parametrize('start_delta', [
    200,  # on the board of an existing WI range
    199,  # inside the existing WI range
])
def test_work_item_update_start_dt_error(session, start_delta):
    now = get_now_timestamp()
    WorkItemFactory(start_timestamp=now+101, end_timestamp=now+200)
    work_item2 = WorkItemFactory(start_timestamp=now+201, end_timestamp=now+301)
    old_start = work_item2.start_timestamp
    update_data = {
        'id': work_item2.id,
        'task': {'id': work_item2.task.id, 'name': work_item2.task.name},
        'start_dt': ts_to_dt(now+start_delta).isoformat(),  # conflict with the first WI range
        'end_dt': ts_to_dt(work_item2.start_timestamp).isoformat(),
    }

    response = client.put(f'/api/work/items/{work_item2.id}', json=update_data)

    assert response.status_code == 400
    assert response.json() == 'The work item with this date and time range already exists.'
    session.refresh(work_item2)
    assert work_item2.start_timestamp == old_start


@pytest.mark.parametrize('end_delta', [
    201,  # on the board of an existing WI range
    202,  # inside the existing WI range
])
def test_work_item_update_end_dt_error(session, end_delta):
    now = get_now_timestamp()
    work_item1 = WorkItemFactory(start_timestamp=now+101, end_timestamp=now+200)
    WorkItemFactory(start_timestamp=now+201, end_timestamp=now+301)
    old_end = work_item1.end_timestamp
    update_data = {
        'id': work_item1.id,
        'task': {'id': work_item1.task.id, 'name': work_item1.task.name},
        'start_dt': ts_to_dt(work_item1.start_timestamp).isoformat(),
        'end_dt': ts_to_dt(now+end_delta).isoformat(),  # conflict with the first WI range
    }

    response = client.put(f'/api/work/items/{work_item1.id}', json=update_data)

    assert response.status_code == 400
    assert response.json() == 'The work item with this date and time range already exists.'
    session.refresh(work_item1)
    assert work_item1.end_timestamp == old_end


def test_work_item_update_conflict_with_current_error(session):
    now = get_now_timestamp()
    work_item = WorkItemFactory(start_timestamp=now+101, end_timestamp=now+200)
    WorkItemFactory(start_timestamp=now+201, end_timestamp=None)  # current WorkItem
    old_end = work_item.end_timestamp
    update_data = {
        'id': work_item.id,
        'task': {'id': work_item.task.id, 'name': work_item.task.name},
        'start_dt': ts_to_dt(work_item.start_timestamp).isoformat(),
        'end_dt': ts_to_dt(now+202).isoformat(),  # conflict with the current WI range
    }

    response = client.put(f'/api/work/items/{work_item.id}', json=update_data)

    assert response.status_code == 400
    assert response.json() == 'The work item with this date and time range already exists.'
    session.refresh(work_item)
    assert work_item.end_timestamp == old_end


@pytest.mark.parametrize('delta', [0, 1])
def test_work_item_update_start_equal_or_more_end_error(session, delta):
    now = get_now_timestamp()
    work_item = WorkItemFactory(start_timestamp=now, end_timestamp=now+100)
    old_start_timestamp = work_item.start_timestamp
    update_data = {
        'id': work_item.id,
        'task': {'id': work_item.task.id, 'name': work_item.task.name},
        'start_dt': ts_to_dt(work_item.end_timestamp+delta).isoformat(),  # update start with the delta
        'end_dt': ts_to_dt(work_item.end_timestamp).isoformat(),
    }

    response = client.put(f'/api/work/items/{work_item.id}', json=update_data)

    assert response.status_code == 400
    assert response.json() == 'The start date and time of the work element must be before its end.'
    session.refresh(work_item)
    assert work_item.start_timestamp == old_start_timestamp
