import importlib.util
import json
from pathlib import Path

import pytest


_MODULE_PATH = Path(__file__).resolve().parents[1] / "app.py"
_MODULE_SPEC = importlib.util.spec_from_file_location("legacy_bike_app", _MODULE_PATH)
app_module = importlib.util.module_from_spec(_MODULE_SPEC)
assert _MODULE_SPEC and _MODULE_SPEC.loader
_MODULE_SPEC.loader.exec_module(app_module)
app = app_module.app
init_db = app_module.init_db
get_bike_with_id = app_module.get_bike_with_id


@pytest.fixture()
def client():
    """Provide a Flask test client for exercising bike routes."""
    with app.test_client() as test_client:
        yield test_client


def test_init_db_returns_bikes():
    bikes = init_db()

    assert len(bikes) == 5
    assert all(bike.is_reserved in (True, False) for bike in bikes)


def test_view_all_available_only_returns_unreserved_bikes(client):
    response = client.get("/view_all_available")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data, "Expected at least one available bike"
    assert all(not bike["is_reserved"] for bike in data)


def test_get_bike_with_id_returns_expected_bike():
    bikes = init_db()
    bike = get_bike_with_id("33", bikes)

    assert bike is not None
    assert bike.id == "33"
    assert bike.is_reserved is True
