import pytest
from starlette.testclient import TestClient

from api import app
from models import Settings, WeekDay

from tests.factories import SettingsFactory


client = TestClient(app)


def test_settings_retrieve(session):
    """Test the settings endpoint."""
    settings = SettingsFactory()

    response = client.get('/api/settings')

    assert response.status_code == 200, response.content
    assert response.json() == {
        'first_day_of_week': settings.first_day_of_week,
        'first_day_of_month': settings.first_day_of_month,
    }


def test_settings_update(session):
    """Test updating the settings endpoint."""
    settings = SettingsFactory(first_day_of_week=WeekDay.Monday, first_day_of_month=1)
    update_data = {
        'first_day_of_week': WeekDay.Friday,
        'first_day_of_month': 15,
    }

    response = client.put('/api/settings', json=update_data)

    assert response.status_code == 200, response.content
    assert response.json() == update_data
    session.refresh(settings)
    assert settings.first_day_of_week == WeekDay.Friday
    assert settings.first_day_of_month == 15


@pytest.mark.parametrize('value', [-1, 0, 32])
def test_settings_update_validation_error(session, value):
    """Test updating settings with an incorrect first_day_of_month value."""
    settings = SettingsFactory(first_day_of_week=WeekDay.Monday, first_day_of_month=15)
    update_data = {
        'first_day_of_week': WeekDay.Friday,
        'first_day_of_month': value,
    }

    response = client.put('/api/settings', json=update_data)

    assert response.status_code == 400
    assert response.json() == 'First day of month must be between 1 and 31.'

    # Verify that the settings were not updated in the database
    session.refresh(settings)
    assert settings.first_day_of_week == WeekDay.Monday
    assert settings.first_day_of_month == 15
