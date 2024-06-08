from starlette.testclient import TestClient

from api import app
from dt import ts_to_dt
from tests.factories import TaskFactory, WorkItemFactory

client = TestClient(app)


def test_work_start(session, frozen_ts):
    # Arrange
    task = TaskFactory()
    expected_start_dt = ts_to_dt(frozen_ts).replace(microsecond=0).isoformat()

    # Act
    response = client.post('/api/work/start', json={'task_id': task.id})

    # Assert
    assert response.status_code == 201
    assert len(task.work_items) == 1
    wi_current = task.work_items[-1]
    assert response.json() == {
        'id': wi_current.id,
        'task': {
            'id': task.id,
            'name': task.name,
        },
        'start_dt': expected_start_dt,
        'end_dt': None,
    }


def test_work_stop_current(session, frozen_ts):
    # Arrange
    task = TaskFactory()
    wi_current = WorkItemFactory(task=task, end_timestamp=None)
    expected_end_timestamp = frozen_ts

    # Act
    response = client.post('/api/work/stop_current')

    # Assert
    assert response.status_code == 200
    assert response.json() == None
    session.refresh(wi_current)
    assert wi_current.end_timestamp == expected_end_timestamp
