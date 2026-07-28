from dataclasses import dataclass, field
from datetime import date
from uuid import uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.dependencies import get_current_user
from app.main import app
from app.models.categoria import Categorias
from app.models.club import Clubes
from app.models.equipo import Equipos
from app.models.jugador import Jugadores
from app.models.plantel import Planteles
from app.models.temporada import Temporadas


@dataclass
class _Role:
    nombre: str


@dataclass
class _User:
    rol: _Role = field(default_factory=lambda: _Role(nombre='Usuario'))


def _build_fallback_entities(db):
    # Crea datos aislados para que el test no dependa del seed global.
    suffix = uuid4().hex[:8]
    club = Clubes(nombre=f'TEST CLUB PLANTEL {suffix}', activo=True)
    categoria = Categorias(nombre=f'TEST CAT PLANTEL {suffix}', sexo='M')

    liga_id = db.query(Temporadas.liga_id).first()
    if not liga_id:
        raise AssertionError('No existe ninguna liga para crear temporada de test')

    temporada = Temporadas(
        liga_id=liga_id[0],
        nombre=f'TEST TEMP PLANTEL {suffix}',
        fecha_inicio=date(2030, 1, 1),
        fecha_fin=date(2030, 12, 31),
        activa=False,
    )

    jugador = Jugadores(
        apellido='TEST',
        nombre='PLANTEL',
        documento=f'TEST-PLANTEL-{suffix}',
        activo=True,
    )

    db.add_all([club, categoria, temporada, jugador])
    db.commit()
    db.refresh(club)
    db.refresh(categoria)
    db.refresh(temporada)
    db.refresh(jugador)

    equipo = Equipos(
        club_id=club.id,
        categoria_id=categoria.id,
        temporada_id=temporada.id,
        nombre=f'TEST EQUIPO PLANTEL {suffix}',
    )
    db.add(equipo)
    db.commit()
    db.refresh(equipo)

    return equipo, jugador


def _find_valid_pair(db):
    equipos = db.query(Equipos).order_by(Equipos.created_at.desc()).all()
    jugadores = db.query(Jugadores).order_by(Jugadores.created_at.desc()).all()
    planteles = db.query(Planteles).all()

    for equipo in equipos:
        for jugador in jugadores:
            if any(p.jugador_id == jugador.id and p.equipo_id == equipo.id for p in planteles):
                continue

            same_season_conflict = False
            for plantel in planteles:
                if plantel.jugador_id != jugador.id:
                    continue
                other_equipo = db.query(Equipos).filter(Equipos.id == plantel.equipo_id).first()
                if other_equipo and other_equipo.temporada_id == equipo.temporada_id:
                    same_season_conflict = True
                    break

            if same_season_conflict:
                continue

            return equipo, jugador

    return _build_fallback_entities(db)


def test_admin_can_create_and_delete_plantel():
    db = SessionLocal()
    try:
        equipo, jugador = _find_valid_pair(db)
        client = TestClient(app)

        created = client.post(
            '/planteles/',
            json={
                'equipo_id': str(equipo.id),
                'jugador_id': str(jugador.id),
                'fecha_desde': '2026-07-27',
                'fecha_hasta': None,
                'dorsal': 77,
                'activo': True,
            },
        )

        assert created.status_code == 201
        plantel_id = created.json()['id']

        deleted = client.delete(f'/planteles/{plantel_id}')
        assert deleted.status_code == 204
    finally:
        db.close()


def test_usuario_without_manage_permission_cannot_create_plantel():
    app.dependency_overrides[get_current_user] = lambda: _User()
    client = TestClient(app)

    response = client.post(
        '/planteles/',
        json={
            'equipo_id': '322bca59-b819-48e9-a529-d75b34cc7568',
            'jugador_id': '6cc835ae-4a9b-4664-85a4-ac6a97fa36a2',
            'fecha_desde': '2026-07-27',
            'fecha_hasta': None,
            'dorsal': 77,
            'activo': True,
        },
    )

    assert response.status_code == 403
    app.dependency_overrides.pop(get_current_user, None)