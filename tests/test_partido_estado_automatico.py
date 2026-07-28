from datetime import date, timedelta
from uuid import uuid4

from app.database import SessionLocal
from app.models.categoria import Categorias
from app.models.club import Clubes
from app.models.equipo import Equipos
from app.models.estado import Estados
from app.models.liga import Ligas
from app.models.temporada import Temporadas
from app.models.tipo_torneo import TiposTorneo
from app.models.torneo import Torneos


def _ensure_estado(db, nombre: str, descripcion: str | None = None) -> Estados:
    estado = db.query(Estados).filter(Estados.nombre == nombre).first()
    if estado:
        return estado
    estado = Estados(nombre=nombre, descripcion=descripcion)
    db.add(estado)
    db.flush()
    return estado


def _build_partido_base_entities() -> dict[str, str]:
    suffix = uuid4().hex[:8]
    db = SessionLocal()
    try:
        liga = db.query(Ligas).order_by(Ligas.created_at.desc()).first()
        if not liga:
            liga = Ligas(nombre=f"Liga-EST-{suffix}")
            db.add(liga)
            db.flush()

        temporada = db.query(Temporadas).filter(Temporadas.liga_id == liga.id).first()
        if not temporada:
            temporada = Temporadas(
                liga_id=liga.id,
                nombre=f"TEMP-EST-{suffix}",
                fecha_inicio=date(2032, 1, 1),
                fecha_fin=date(2032, 12, 31),
                activa=False,
            )
            db.add(temporada)
            db.flush()

        categoria = db.query(Categorias).order_by(Categorias.created_at.asc()).first()
        if not categoria:
            categoria = Categorias(nombre=f"CAT-EST-{suffix}", sexo="M")
            db.add(categoria)
            db.flush()

        tipo_torneo = db.query(TiposTorneo).order_by(TiposTorneo.created_at.asc()).first()
        if not tipo_torneo:
            tipo_torneo = TiposTorneo(nombre=f"Tipo-EST-{suffix}")
            db.add(tipo_torneo)
            db.flush()

        club_local = Clubes(nombre=f"Club Local EST {suffix}")
        club_visitante = Clubes(nombre=f"Club Visitante EST {suffix}")
        db.add(club_local)
        db.add(club_visitante)
        db.flush()

        equipo_local = Equipos(
            club_id=club_local.id,
            temporada_id=temporada.id,
            categoria_id=categoria.id,
            nombre=f"Equipo Local EST {suffix}",
        )
        equipo_visitante = Equipos(
            club_id=club_visitante.id,
            temporada_id=temporada.id,
            categoria_id=categoria.id,
            nombre=f"Equipo Visitante EST {suffix}",
        )
        db.add(equipo_local)
        db.add(equipo_visitante)
        db.flush()

        torneo = Torneos(
            temporada_id=temporada.id,
            categoria_id=categoria.id,
            tipo_torneo_id=tipo_torneo.id,
            nombre=f"Torneo EST {suffix}",
            fecha_inicio=date(2032, 2, 1),
            fecha_fin=date(2032, 11, 30),
            activo=True,
        )
        db.add(torneo)

        programado = _ensure_estado(db, "Programado", "Estado inicial")
        finalizado = _ensure_estado(db, "Finalizado", "Partido concluido")
        suspendido = _ensure_estado(db, "Suspendido", "Partido suspendido")
        db.commit()

        return {
            "torneo_id": str(torneo.id),
            "equipo_local_id": str(equipo_local.id),
            "equipo_visitante_id": str(equipo_visitante.id),
            "programado_id": str(programado.id),
            "finalizado_id": str(finalizado.id),
            "suspendido_id": str(suspendido.id),
        }
    finally:
        db.close()


def test_partido_future_date_defaults_to_programado(client):
    entities = _build_partido_base_entities()
    future_date = date.today() + timedelta(days=2)

    response = client.post(
        "/partidos/",
        json={
            "torneo_id": entities["torneo_id"],
            "equipo_local_id": entities["equipo_local_id"],
            "equipo_visitante_id": entities["equipo_visitante_id"],
            "fecha_partido": future_date.isoformat(),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["estado_id"] == entities["programado_id"]


def test_partido_today_or_past_defaults_to_finalizado(client):
    entities = _build_partido_base_entities()

    response = client.post(
        "/partidos/",
        json={
            "torneo_id": entities["torneo_id"],
            "equipo_local_id": entities["equipo_local_id"],
            "equipo_visitante_id": entities["equipo_visitante_id"],
            "fecha_partido": date.today().isoformat(),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["estado_id"] == entities["finalizado_id"]


def test_partido_manual_suspendido_is_preserved_on_auto_updates(client):
    entities = _build_partido_base_entities()
    future_date = date.today() + timedelta(days=3)

    create_response = client.post(
        "/partidos/",
        json={
            "torneo_id": entities["torneo_id"],
            "equipo_local_id": entities["equipo_local_id"],
            "equipo_visitante_id": entities["equipo_visitante_id"],
            "fecha_partido": future_date.isoformat(),
            "estado_id": entities["suspendido_id"],
            "estado_manual": True,
        },
    )
    assert create_response.status_code == 200
    partido_id = create_response.json()["id"]

    update_response = client.put(
        f"/partidos/{partido_id}",
        json={
            "observaciones": "Se mantiene suspendido por decision manual",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["estado_id"] == entities["suspendido_id"]


def test_partido_estado_manual_requires_estado_id(client):
    entities = _build_partido_base_entities()
    future_date = date.today() + timedelta(days=4)

    response = client.post(
        "/partidos/",
        json={
            "torneo_id": entities["torneo_id"],
            "equipo_local_id": entities["equipo_local_id"],
            "equipo_visitante_id": entities["equipo_visitante_id"],
            "fecha_partido": future_date.isoformat(),
            "estado_manual": True,
        },
    )

    assert response.status_code == 400
    assert "estado_manual" in response.json()["detail"]