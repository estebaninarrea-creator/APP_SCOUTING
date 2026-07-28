from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_current_user
from app.main import app

pytestmark = pytest.mark.no_regression


@dataclass
class _Role:
    nombre: str


@dataclass
class _User:
    rol: _Role | None


def _set_role_override(role_name: str | None) -> None:
    if role_name is None:
        app.dependency_overrides.pop(get_current_user, None)
        return
    app.dependency_overrides[get_current_user] = lambda: _User(rol=_Role(nombre=role_name))


@pytest.mark.parametrize(
    "path,expected_status",
    [
        ("/dashboard/summary", 401),
        ("/jugadores/", 401),
        ("/roles/", 401),
        ("/scouting/informes", 401),
    ],
)
def test_anon_contract_requires_auth(path: str, expected_status: int):
    _set_role_override(None)
    client = TestClient(app)

    response = client.get(path)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role_name,path,expected_status",
    [
        # Dashboard
        ("Admin", "/dashboard/summary", 200),
        ("Scout", "/dashboard/summary", 200),
        ("Usuario", "/dashboard/summary", 200),
        # Admin-only endpoints
        ("Admin", "/roles/", 200),
        ("Scout", "/roles/", 403),
        ("Usuario", "/roles/", 403),
        ("Admin", "/clubes/", 200),
        ("Scout", "/clubes/", 403),
        ("Usuario", "/clubes/", 403),
        ("Admin", "/maestros/", 200),
        ("Scout", "/maestros/", 403),
        ("Usuario", "/maestros/", 403),
        ("Admin", "/torneos_clubes/", 200),
        ("Scout", "/torneos_clubes/", 403),
        ("Usuario", "/torneos_clubes/", 403),
        ("Admin", "/usuarios_ligas/", 200),
        ("Scout", "/usuarios_ligas/", 403),
        ("Usuario", "/usuarios_ligas/", 403),
        ("Admin", "/formacion_jugadores/", 200),
        ("Scout", "/formacion_jugadores/", 403),
        ("Usuario", "/formacion_jugadores/", 403),
        # Read endpoints by role
        ("Admin", "/equipos/", 200),
        ("Scout", "/equipos/", 403),
        ("Usuario", "/equipos/", 200),
        ("Admin", "/jugadores/", 200),
        ("Scout", "/jugadores/", 200),
        ("Usuario", "/jugadores/", 200),
        ("Admin", "/torneos/", 200),
        ("Scout", "/torneos/", 200),
        ("Usuario", "/torneos/", 200),
        ("Admin", "/partidos/", 200),
        ("Scout", "/partidos/", 200),
        ("Usuario", "/partidos/", 200),
        ("Admin", "/planteles/", 200),
        ("Scout", "/planteles/", 200),
        ("Usuario", "/planteles/", 200),
        ("Admin", "/scouts/", 200),
        ("Scout", "/scouts/", 200),
        ("Usuario", "/scouts/", 403),
        ("Admin", "/scouting/informes", 200),
        ("Scout", "/scouting/informes", 200),
        ("Usuario", "/scouting/informes", 403),
    ],
)
def test_role_endpoint_contracts(role_name: str, path: str, expected_status: int):
    _set_role_override(role_name)
    client = TestClient(app)

    response = client.get(path)

    assert response.status_code == expected_status


def test_public_endpoints_contract():
    # / and /health/database no dependen de token.
    _set_role_override(None)
    client = TestClient(app)

    root = client.get("/")
    health = client.get("/health/database")

    assert root.status_code == 200
    assert health.status_code == 200
