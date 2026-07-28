import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.torneo import Torneos
from app.schemas.torneo import TorneoCreate, TorneoUpdate

logger = logging.getLogger(__name__)


def get_torneos(db: Session):
    logger.info("Obteniendo todos los torneos")
    try:
        result = db.query(Torneos).order_by(Torneos.nombre).all()
        logger.info(f"Se obtuvieron {len(result)} torneos")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener torneos: {str(e)}")
        raise


def get_torneo(db: Session, torneo_id: UUID):
    logger.info(f"Obteniendo torneo {torneo_id}")
    try:
        result = db.query(Torneos).filter(Torneos.id == torneo_id).first()
        if result:
            logger.info(f"Torneo encontrado: {torneo_id}")
        else:
            logger.warning(f"Torneo no encontrado: {torneo_id}")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener torneo {torneo_id}: {str(e)}")
        raise


def create_torneo(db: Session, torneo: TorneoCreate):
    logger.info(f"Creando nuevo torneo")
    try:
        nuevo = Torneos(**torneo.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Torneo creado: {nuevo.id}")
        return nuevo
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear torneo: {str(e)}")
        raise


def update_torneo(db: Session, torneo_id: UUID, torneo: TorneoUpdate):
    logger.info(f"Actualizando torneo {torneo_id}")
    try:
        existing = get_torneo(db, torneo_id)
        if not existing:
            logger.warning(f"Torneo no encontrado para actualizar: {torneo_id}")
            return None
        for key, value in torneo.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Torneo actualizado: {torneo_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar torneo {torneo_id}: {str(e)}")
        raise


def delete_torneo(db: Session, torneo_id: UUID):
    logger.info(f"Eliminando torneo {torneo_id}")
    try:
        existing = get_torneo(db, torneo_id)
        if existing:
            db.delete(existing)
            db.commit()
            logger.info(f"Torneo eliminado: {torneo_id}")
        else:
            logger.warning(f"Torneo no encontrado para eliminar: {torneo_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar torneo {torneo_id}: {str(e)}")
        raise
