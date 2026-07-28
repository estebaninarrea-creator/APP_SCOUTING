import pytest
from fastapi.testclient import TestClient
from app.main import app

pytestmark = pytest.mark.no_regression

client = TestClient(app)


def test_root_and_health():
    response = client.get('/')
    assert response.status_code == 200

    db_response = client.get('/health/database')
    assert db_response.status_code == 200
