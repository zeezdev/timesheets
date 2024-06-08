from starlette.testclient import TestClient

from api import app
from models import Category
from tests.factories import CategoryFactory

client = TestClient(app)


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
