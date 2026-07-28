"""Tests de integración CRUD sobre endpoints protegidos con auth override."""

import pytest


pytestmark = pytest.mark.no_regression


def test_arbitros(client):
    response = client.get("/arbitros/")
    assert response.status_code == 200

    create_payload = {
        "nombre": "Juan",
        "apellido": "Perez",
        "documento": "12345678",
        "liga_id": None,
        "activo": True,
    }
    created = client.post("/arbitros/", json=create_payload)
    assert created.status_code == 201
    arbitro_id = created.json()["id"]

    detail = client.get(f"/arbitros/{arbitro_id}")
    assert detail.status_code == 200

    updated = client.put(f"/arbitros/{arbitro_id}", json={"nombre": "Juan Updated"})
    assert updated.status_code == 200
    assert updated.json()["nombre"] == "Juan Updated"

    deleted = client.delete(f"/arbitros/{arbitro_id}")
    assert deleted.status_code == 204


def test_categorias(client):
    response = client.get("/categorias/")
    assert response.status_code == 200

    create_payload = {
        "nombre": "U20",
        "sexo": "M",
        "edad_min": 18,
        "edad_max": 20,
    }
    created = client.post("/categorias/", json=create_payload)
    assert created.status_code == 201
    categoria_id = created.json()["id"]

    detail = client.get(f"/categorias/{categoria_id}")
    assert detail.status_code == 200

    updated = client.put(f"/categorias/{categoria_id}", json={"edad_max": 21})
    assert updated.status_code == 200
    assert updated.json()["edad_max"] == 21

    deleted = client.delete(f"/categorias/{categoria_id}")
    assert deleted.status_code == 204


def test_tipos_torneo(client):
    response = client.get("/tipos_torneo/")
    assert response.status_code == 200

    created = client.post("/tipos_torneo/", json={"nombre": "Friendly"})
    assert created.status_code == 201
    tipo_id = created.json()["id"]

    detail = client.get(f"/tipos_torneo/{tipo_id}")
    assert detail.status_code == 200

    updated = client.put(f"/tipos_torneo/{tipo_id}", json={"nombre": "Friendly Updated"})
    assert updated.status_code == 200
    assert updated.json()["nombre"] == "Friendly Updated"

    deleted = client.delete(f"/tipos_torneo/{tipo_id}")
    assert deleted.status_code == 204


def test_error_handling(client):
    response = client.get("/arbitros/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

    bad_payload = {"nombre": ""}
    invalid = client.post("/arbitros/", json=bad_payload)
    assert invalid.status_code in (400, 422)
