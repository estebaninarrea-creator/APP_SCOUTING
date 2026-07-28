import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.equipo import Equipos
from app.models.partido import Partidos
from app.models.torneo import Torneos
from app.models.torneo_club import TorneosClubes
from app.config import settings
from app.schemas.partido import PartidoCreate, PartidoUpdate

logger = logging.getLogger(__name__)


def _map_partido_payload(payload: dict) -> dict:
    """Normaliza nombres de campos de schema al modelo SQLAlchemy."""
    if "local_equipo_id" in payload:
        payload["equipo_local_id"] = payload.pop("local_equipo_id")
    if "visitante_equipo_id" in payload:
        payload["equipo_visitante_id"] = payload.pop("visitante_equipo_id")
    return payload


def _validate_partido_relations(
    db: Session,
    torneo_id: UUID | None,
    equipo_local_id: UUID | None,
    equipo_visitante_id: UUID | None,
):
    if equipo_local_id and equipo_visitante_id and equipo_local_id == equipo_visitante_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El equipo local y el equipo visitante no pueden ser el mismo",
        )

    equipo_local = None
    equipo_visitante = None

    if equipo_local_id:
        equipo_local = db.query(Equipos).filter(Equipos.id == equipo_local_id).first()
        if not equipo_local:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipo local no encontrado",
            )

    if equipo_visitante_id:
        equipo_visitante = db.query(Equipos).filter(Equipos.id == equipo_visitante_id).first()
        if not equipo_visitante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipo visitante no encontrado",
            )

    # Independientemente de que haya torneo, ambos equipos deben compartir
    # temporada y categoría para que el partido sea consistente.
    if equipo_local and equipo_visitante:
        if (
            equipo_local.temporada_id != equipo_visitante.temporada_id
            or equipo_local.categoria_id != equipo_visitante.categoria_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los equipos local y visitante deben pertenecer a la misma temporada y categoría",
            )

    if not torneo_id:
        return

    torneo = db.query(Torneos).filter(Torneos.id == torneo_id).first()
    if not torneo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Torneo no encontrado",
        )

    if equipo_local and (
        equipo_local.temporada_id != torneo.temporada_id
        or equipo_local.categoria_id != torneo.categoria_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El equipo local no pertenece a la misma temporada y categoría del torneo",
        )

    if equipo_visitante and (
        equipo_visitante.temporada_id != torneo.temporada_id
        or equipo_visitante.categoria_id != torneo.categoria_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El equipo visitante no pertenece a la misma temporada y categoría del torneo",
        )

    if not settings.ENFORCE_TORNEO_CLUB_MEMBERSHIP:
        return

    for team_id, team_label in (
        (equipo_local_id, "local"),
        (equipo_visitante_id, "visitante"),
    ):
        if not team_id:
            continue
        membership = (
            db.query(TorneosClubes)
            .filter(
                TorneosClubes.torneo_id == torneo_id,
                TorneosClubes.equipo_id == team_id,
            )
            .first()
        )
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El equipo {team_label} no está registrado en torneos_clubes para el torneo indicado",
            )


def _resolve_partido_relations(existing: Partidos | None, payload: dict) -> tuple[UUID | None, UUID | None, UUID | None]:
    torneo_id = payload.get("torneo_id", getattr(existing, "torneo_id", None))
    equipo_local_id = payload.get("equipo_local_id", getattr(existing, "equipo_local_id", None))
    equipo_visitante_id = payload.get("equipo_visitante_id", getattr(existing, "equipo_visitante_id", None))
    return torneo_id, equipo_local_id, equipo_visitante_id


def get_partidos(db: Session):
    logger.info("Obteniendo todos los partidos")
    try:
        result = db.query(Partidos).order_by(Partidos.fecha_partido).all()
        logger.info(f"Se obtuvieron {len(result)} partidos")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener partidos: {str(e)}")
        raise


def get_partido(db: Session, partido_id: UUID):
    logger.info(f"Obteniendo partido {partido_id}")
    try:
        result = db.query(Partidos).filter(Partidos.id == partido_id).first()
        if result:
            logger.info(f"Partido encontrado: {partido_id}")
        else:
            logger.warning(f"Partido no encontrado: {partido_id}")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener partido {partido_id}: {str(e)}")
        raise


def create_partido(db: Session, partido: PartidoCreate):
    logger.info(f"Creando nuevo partido")
    try:
        payload = _map_partido_payload(partido.model_dump())
        torneo_id, equipo_local_id, equipo_visitante_id = _resolve_partido_relations(None, payload)
        _validate_partido_relations(db, torneo_id, equipo_local_id, equipo_visitante_id)
        nuevo = Partidos(**payload)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Partido creado: {nuevo.id}")
        return nuevo
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear partido: {str(e)}")
        raise


def update_partido(db: Session, partido_id: UUID, partido: PartidoUpdate):
    logger.info(f"Actualizando partido {partido_id}")
    try:
        existing = get_partido(db, partido_id)
        if not existing:
            logger.warning(f"Partido no encontrado para actualizar: {partido_id}")
            return None
        payload = _map_partido_payload(partido.model_dump(exclude_unset=True))
        torneo_id, equipo_local_id, equipo_visitante_id = _resolve_partido_relations(existing, payload)
        _validate_partido_relations(db, torneo_id, equipo_local_id, equipo_visitante_id)
        for key, value in payload.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Partido actualizado: {partido_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar partido {partido_id}: {str(e)}")
        raise


def delete_partido(db: Session, partido_id: UUID):
    logger.info(f"Eliminando partido {partido_id}")
    try:
        existing = get_partido(db, partido_id)
        if existing:
            db.delete(existing)
            db.commit()
            logger.info(f"Partido eliminado: {partido_id}")
        else:
            logger.warning(f"Partido no encontrado para eliminar: {partido_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar partido {partido_id}: {str(e)}")
        raise
