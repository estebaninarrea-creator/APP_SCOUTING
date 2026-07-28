import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.temporada import Temporadas
from app.schemas.temporada import TemporadaCreate, TemporadaUpdate

logger = logging.getLogger(__name__)


def get_temporadas(db: Session):
    logger.info("Obteniendo todas las temporadas")
    try:
        result = db.query(Temporadas).order_by(Temporadas.nombre).all()
        logger.info(f"Se obtuvieron {len(result)} temporadas")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener temporadas: {str(e)}")
        raise


def get_temporada(db: Session, temporada_id: UUID):
    logger.info(f"Obteniendo temporada {temporada_id}")
    try:
        result = db.query(Temporadas).filter(Temporadas.id == temporada_id).first()
        if result:
            logger.info(f"Temporada encontrada: {temporada_id}")
        else:
            logger.warning(f"Temporada no encontrada: {temporada_id}")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener temporada {temporada_id}: {str(e)}")
        raise


def create_temporada(db: Session, temporada: TemporadaCreate):
    logger.info(f"Creando nueva temporada")
    try:
        nuevo = Temporadas(**temporada.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Temporada creada: {nuevo.id}")
        return nuevo
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear temporada: {str(e)}")
        raise


def update_temporada(db: Session, temporada_id: UUID, temporada: TemporadaUpdate):
    logger.info(f"Actualizando temporada {temporada_id}")
    try:
        existing = get_temporada(db, temporada_id)
        if not existing:
            logger.warning(f"Temporada no encontrada para actualizar: {temporada_id}")
            return None
        for key, value in temporada.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Temporada actualizada: {temporada_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar temporada {temporada_id}: {str(e)}")
        raise


def delete_temporada(db: Session, temporada_id: UUID):
    logger.info(f"Eliminando temporada {temporada_id}")
    try:
        existing = get_temporada(db, temporada_id)
        if existing:
            db.delete(existing)
            db.commit()
            logger.info(f"Temporada eliminada: {temporada_id}")
        else:
            logger.warning(f"Temporada no encontrada para eliminar: {temporada_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar temporada {temporada_id}: {str(e)}")
        raise
