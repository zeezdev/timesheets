import pytest
from starlette.testclient import TestClient

from api import app
from models import Task
from tests.factories import TaskFactory, CategoryFactory, WorkItemFactory

client = TestClient(app)


def test_tasks_list(session):
    # Arrange
    task1 = TaskFactory()
    task2 = TaskFactory()
    WorkItemFactory(task=task2)
    task3 = TaskFactory()
    WorkItemFactory(task=task3, end_timestamp=None)
    tasks = sorted([task1, task2, task3], key=lambda t: t.id, reverse=True)

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
            'is_current': bool(t.id == task3.id),
            'is_archived': t.is_archived,
        } for t in sorted(tasks, key=lambda t: t.id, reverse=True)
    ]


@pytest.mark.parametrize('filter_value', [True, False])
def test_tasks_list_filter_by_is_archived(session, filter_value):
    # Arrange
    tasks = [
        TaskFactory(is_archived=filter_value),
        TaskFactory(is_archived=not filter_value),
        TaskFactory(is_archived=filter_value),
    ]
    expected_ids = sorted([tasks[0].id, tasks[2].id])

    # Act
    response = client.get('/api/tasks', params={'is_archived': filter_value})

    # Arrange
    assert response.status_code == 200
    assert sorted([x['id'] for x in response.json()]) == expected_ids


@pytest.mark.parametrize('filter_value', [True, False])
def test_tasks_list_filter_by_is_current(session, filter_value):
    # Arrange
    task1 = TaskFactory()
    task2 = TaskFactory()
    task3 = WorkItemFactory(end_timestamp=None).task  # current
    if filter_value:
        expected_ids = [task3.id]
    else:
        expected_ids = sorted([task1.id, task2.id])

    # Act
    response = client.get('/api/tasks', params={'is_current': filter_value})

    # Arrange
    assert response.status_code == 200
    assert sorted([x['id'] for x in response.json()]) == expected_ids


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
