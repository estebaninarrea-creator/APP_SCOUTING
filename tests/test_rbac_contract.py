from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_current_user
from app.main import app

pytestmark = pytest.mark.no_regression


@dataclass
class _DummyRole:
    nombre: str


@dataclass
class _DummyUser:
    rol: _DummyRole | None


def _make_user(role_name: str | None) -> _DummyUser:
    return _DummyUser(rol=_DummyRole(nombre=role_name) if role_name else None)


def test_protected_endpoint_requires_token():
    # Force una request sin usuario override para validar contrato 401.
    app.dependency_overrides.pop(get_current_user, None)
    client = TestClient(app)

    response = client.get('/jugadores/')

    assert response.status_code == 401


def test_usuario_role_forbidden_on_admin_endpoint():
    usuario = _make_user('Usuario')
    app.dependency_overrides[get_current_user] = lambda: usuario
    client = TestClient(app)

    response = client.get('/roles/')

    assert response.status_code == 403
    app.dependency_overrides.pop(get_current_user, None)


def test_usuario_role_allowed_on_dashboard_summary():
    usuario = _make_user('Usuario')
    app.dependency_overrides[get_current_user] = lambda: usuario
    client = TestClient(app)

    response = client.get('/dashboard/summary')

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get('jugadores'), int)
    assert isinstance(body.get('roles'), int)
    assert isinstance(body.get('partidos'), int)
    assert isinstance(body.get('clubes'), int)
    app.dependency_overrides.pop(get_current_user, None)
