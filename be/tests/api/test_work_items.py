from starlette.testclient import TestClient

from api import app
from dt import ts_to_dt
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
        'id': work_item.id,
        'task': {'id': new_task.id, 'name': new_task.name},
    }

    response = client.patch(f'/api/work/items/{work_item.id}', json=update_data)

    assert response.status_code == 200
    assert response.json() == {
        'start_dt': ts_to_dt(old_start).isoformat(),
        'end_dt': ts_to_dt(old_end).isoformat(),
        **update_data,
    }
    session.refresh(work_item)
    assert work_item.start_timestamp == old_start
    assert work_item.end_timestamp == old_end
    assert work_item.task == new_task
