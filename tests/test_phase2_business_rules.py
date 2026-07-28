from datetime import date
from uuid import uuid4

from app.config import settings
from app.database import SessionLocal
from app.models.categoria import Categorias
from app.models.club import Clubes
from app.models.equipo import Equipos
from app.models.formacion import Formaciones
from app.models.jugador import Jugadores
from app.models.liga import Ligas
from app.models.partido import Partidos
from app.models.plantel import Planteles
from app.models.temporada import Temporadas
from app.models.tipo_torneo import TiposTorneo
from app.models.torneo import Torneos


def _build_phase2_entities():
    suffix = uuid4().hex[:8]
    db = SessionLocal()
    try:
        liga = db.query(Ligas).order_by(Ligas.created_at.desc()).first()
        if not liga:
            liga = Ligas(nombre=f"Liga-P2-{suffix}")
            db.add(liga)
            db.flush()

        temporada = db.query(Temporadas).filter(Temporadas.liga_id == liga.id).first()
        if not temporada:
            temporada = Temporadas(
                liga_id=liga.id,
                nombre=f"TEMP-P2-{suffix}",
                fecha_inicio=date(2031, 1, 1),
                fecha_fin=date(2031, 12, 31),
                activa=False,
            )
            db.add(temporada)
            db.flush()

        categoria = db.query(Categorias).order_by(Categorias.created_at.asc()).first()
        if not categoria:
            categoria = Categorias(nombre=f"CAT-P2-{suffix}", sexo="M")
            db.add(categoria)
            db.flush()

        tipo_torneo = db.query(TiposTorneo).order_by(TiposTorneo.created_at.asc()).first()
        if not tipo_torneo:
            tipo_torneo = TiposTorneo(nombre=f"Tipo-P2-{suffix}")
            db.add(tipo_torneo)
            db.flush()

        club_local = Clubes(nombre=f"Club Local P2 {suffix}")
        club_visitante = Clubes(nombre=f"Club Visitante P2 {suffix}")
        db.add(club_local)
        db.add(club_visitante)
        db.flush()

        equipo_local = Equipos(
            club_id=club_local.id,
            temporada_id=temporada.id,
            categoria_id=categoria.id,
            nombre=f"Equipo Local P2 {suffix}",
        )
        equipo_visitante = Equipos(
            club_id=club_visitante.id,
            temporada_id=temporada.id,
            categoria_id=categoria.id,
            nombre=f"Equipo Visitante P2 {suffix}",
        )
        db.add(equipo_local)
        db.add(equipo_visitante)
        db.flush()

        torneo = Torneos(
            temporada_id=temporada.id,
            categoria_id=categoria.id,
            tipo_torneo_id=tipo_torneo.id,
            nombre=f"Torneo P2 {suffix}",
            fecha_inicio=date(2031, 2, 1),
            fecha_fin=date(2031, 11, 30),
            activo=True,
        )
        db.add(torneo)
        db.flush()

        partido = Partidos(
            torneo_id=torneo.id,
            equipo_local_id=equipo_local.id,
            equipo_visitante_id=equipo_visitante.id,
            fecha_partido=date(2031, 6, 15),
        )
        db.add(partido)
        db.flush()

        formacion = Formaciones(
            partido_id=partido.id,
            equipo_id=equipo_local.id,
            esquema="4-3-3",
        )
        db.add(formacion)
        db.flush()

        jugador_en_plantel = Jugadores(
            apellido=f"ApellidoIn{suffix}",
            nombre=f"NombreIn{suffix}",
            documento=f"DOC-IN-{suffix}",
            activo=True,
        )
        jugador_fuera_plantel = Jugadores(
            apellido=f"ApellidoOut{suffix}",
            nombre=f"NombreOut{suffix}",
            documento=f"DOC-OUT-{suffix}",
            activo=True,
        )
        db.add(jugador_en_plantel)
        db.add(jugador_fuera_plantel)
        db.flush()

        plantel = Planteles(
            equipo_id=equipo_local.id,
            jugador_id=jugador_en_plantel.id,
            fecha_desde=date(2031, 1, 1),
            fecha_hasta=None,
            activo=True,
            dorsal=9,
        )
        db.add(plantel)
        db.commit()

        return {
            "torneo_id": str(torneo.id),
            "equipo_local_id": str(equipo_local.id),
            "equipo_visitante_id": str(equipo_visitante.id),
            "formacion_id": str(formacion.id),
            "jugador_en_plantel_id": str(jugador_en_plantel.id),
            "jugador_fuera_plantel_id": str(jugador_fuera_plantel.id),
        }
    finally:
        db.close()


def test_partido_allows_teams_not_in_torneos_clubes_by_default(client):
    entities = _build_phase2_entities()

    previous = settings.ENFORCE_TORNEO_CLUB_MEMBERSHIP
    settings.ENFORCE_TORNEO_CLUB_MEMBERSHIP = False
    try:
        response = client.post(
            "/partidos/",
            json={
                "torneo_id": entities["torneo_id"],
                "equipo_local_id": entities["equipo_local_id"],
                "equipo_visitante_id": entities["equipo_visitante_id"],
                "fecha_partido": "2031-06-20",
            },
        )
        assert response.status_code == 200
    finally:
        settings.ENFORCE_TORNEO_CLUB_MEMBERSHIP = previous


def test_partido_blocks_teams_not_in_torneos_clubes_when_flag_enabled(client):
    entities = _build_phase2_entities()

    previous = settings.ENFORCE_TORNEO_CLUB_MEMBERSHIP
    settings.ENFORCE_TORNEO_CLUB_MEMBERSHIP = True
    try:
        response = client.post(
            "/partidos/",
            json={
                "torneo_id": entities["torneo_id"],
                "equipo_local_id": entities["equipo_local_id"],
                "equipo_visitante_id": entities["equipo_visitante_id"],
                "fecha_partido": "2031-06-21",
            },
        )
        assert response.status_code == 400
        assert "torneos_clubes" in response.json()["detail"]
    finally:
        settings.ENFORCE_TORNEO_CLUB_MEMBERSHIP = previous


def test_formacion_jugadores_requires_active_roster_membership(client):
    entities = _build_phase2_entities()

    invalid_response = client.post(
        "/formacion_jugadores/",
        json={
            "formacion_id": entities["formacion_id"],
            "jugador_id": entities["jugador_fuera_plantel_id"],
            "numero_camiseta": 15,
        },
    )
    assert invalid_response.status_code == 400
    assert "plantel activo" in invalid_response.json()["detail"]

    valid_response = client.post(
        "/formacion_jugadores/",
        json={
            "formacion_id": entities["formacion_id"],
            "jugador_id": entities["jugador_en_plantel_id"],
            "numero_camiseta": 9,
        },
    )
    assert valid_response.status_code == 201