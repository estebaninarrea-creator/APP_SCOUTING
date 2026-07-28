import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.plantel import Planteles
from app.models.partido import Partidos
from app.models.partido_jugador import PartidoJugadores
from app.models.jugador import Jugadores
from app.schemas.partido_jugador import PartidoJugadorCreate, PartidoJugadorUpdate

logger = logging.getLogger(__name__)


def _validate_jugador_en_plantel_activo(db: Session, partido: Partidos, jugador_id: UUID) -> None:
    if not partido.equipo_local_id and not partido.equipo_visitante_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El partido debe tener equipos asignados para convocar jugadores",
        )

    equipos_partido = [equipo_id for equipo_id in (partido.equipo_local_id, partido.equipo_visitante_id) if equipo_id]

    query = (
        db.query(Planteles)
        .filter(
            Planteles.jugador_id == jugador_id,
            Planteles.equipo_id.in_(equipos_partido),
            Planteles.activo.is_(True),
        )
    )

    if partido.fecha_partido:
        query = query.filter(
            Planteles.fecha_desde <= partido.fecha_partido,
            or_(Planteles.fecha_hasta.is_(None), Planteles.fecha_hasta >= partido.fecha_partido),
        )

    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El jugador no pertenece a un plantel activo del partido",
        )


def get_partido_jugadores(db: Session, partido_id: UUID) -> list[PartidoJugadores]:
    try:
        return (
            db.query(PartidoJugadores)
            .filter(PartidoJugadores.partido_id == partido_id)
            .order_by(PartidoJugadores.created_at.desc())
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugadores del partido {partido_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener jugadores del partido")


def get_partido_jugador(db: Session, partido_id: UUID, partido_jugador_id: UUID) -> PartidoJugadores:
    try:
        result = (
            db.query(PartidoJugadores)
            .filter(PartidoJugadores.partido_id == partido_id, PartidoJugadores.id == partido_jugador_id)
            .first()
        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador del partido no encontrado")
        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugador del partido {partido_jugador_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener jugador del partido")


def create_partido_jugador(db: Session, partido_id: UUID, payload: PartidoJugadorCreate) -> PartidoJugadores:
    try:
        partido = db.query(Partidos).filter(Partidos.id == partido_id).first()
        if not partido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")

        jugador = db.query(Jugadores).filter(Jugadores.id == payload.jugador_id).first()
        if not jugador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")

        _validate_jugador_en_plantel_activo(db, partido, payload.jugador_id)

        existing = (
            db.query(PartidoJugadores)
            .filter(PartidoJugadores.partido_id == partido_id, PartidoJugadores.jugador_id == payload.jugador_id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El jugador ya está asignado al partido")

        nuevo = PartidoJugadores(
            partido_id=partido_id,
            jugador_id=payload.jugador_id,
            numero_camiseta=payload.numero_camiseta,
            posicion=payload.posicion,
            minutos_jugados=payload.minutos_jugados,
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al crear jugador del partido: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al asignar jugador al partido")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear jugador del partido: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al asignar jugador al partido")


def update_partido_jugador(db: Session, partido_id: UUID, partido_jugador_id: UUID, payload: PartidoJugadorUpdate) -> PartidoJugadores:
    try:
        existing = get_partido_jugador(db, partido_id, partido_jugador_id)
        partido = db.query(Partidos).filter(Partidos.id == partido_id).first()
        if not partido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")

        update_data = payload.model_dump(exclude_unset=True)
        jugador_id = update_data.get("jugador_id", existing.jugador_id)
        jugador = db.query(Jugadores).filter(Jugadores.id == jugador_id).first()
        if not jugador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
        _validate_jugador_en_plantel_activo(db, partido, jugador_id)

        for key, value in update_data.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al actualizar jugador del partido: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar jugador del partido")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar jugador del partido: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar jugador del partido")


def delete_partido_jugador(db: Session, partido_id: UUID, partido_jugador_id: UUID) -> None:
    try:
        existing = get_partido_jugador(db, partido_id, partido_jugador_id)
        db.delete(existing)
        db.commit()
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar jugador del partido: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar jugador del partido")
