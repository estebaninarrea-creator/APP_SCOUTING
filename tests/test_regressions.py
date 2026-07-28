import pytest

from app.database import SessionLocal
from app.models.jugador import Jugadores
from app.models.posicion import Posiciones
from app.models.usuario import Usuarios

pytestmark = pytest.mark.no_regression


def test_maestros_endpoint_returns_positions_payload(client):
    response = client.get('/maestros/')

    assert response.status_code == 200
    body = response.json()
    assert 'provincias' in body
    assert 'ciudades' in body
    assert 'posiciones' in body
    assert isinstance(body['posiciones'], list)


def test_update_jugador_accepts_positions_as_dict_payload(client):
    db = SessionLocal()
    try:
        jugador = db.query(Jugadores).order_by(Jugadores.created_at.desc()).first()
        posicion = db.query(Posiciones).order_by(Posiciones.nombre).first()
        usuario = db.query(Usuarios).order_by(Usuarios.created_at.desc()).first()

        assert jugador is not None
        assert posicion is not None
        assert usuario is not None

        response = client.put(
            f'/jugadores/{jugador.id}',
            json={
                'apellido': jugador.apellido,
                'nombre': jugador.nombre,
                'posiciones': [
                    {'id': str(posicion.id), 'principal': True}
                ],
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body['id'] == str(jugador.id)
        assert body['posiciones'][0]['id'] == str(posicion.id)
    finally:
        db.close()
