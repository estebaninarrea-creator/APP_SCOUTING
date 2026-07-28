from datetime import datetime, UTC
from uuid import UUID
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

from app.models.liga import Ligas
from app.schemas.liga import LigaCreate, LigaUpdate

logger = logging.getLogger(__name__)


def get_ligas(db: Session):
    logger.info("Obteniendo todas las ligas")
    try:
        result = db.query(Ligas).filter(Ligas.deleted_at.is_(None)).order_by(Ligas.nombre).all()
        logger.info(f"Se obtuvieron {len(result)} ligas")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener ligas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener ligas"
        )


def get_liga(db: Session, liga_id: UUID):
    logger.info(f"Obteniendo liga {liga_id}")
    try:
        result = db.query(Ligas).filter(Ligas.id == liga_id, Ligas.deleted_at.is_(None)).first()
        if not result:
            logger.warning(f"Liga no encontrada: {liga_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Liga no encontrada"
            )
        logger.info(f"Liga encontrada: {liga_id}")
        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener liga {liga_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener liga"
        )


def create_liga(db: Session, liga: LigaCreate):
    logger.info(f"Creando nueva liga")
    try:
        nuevo = Ligas(**liga.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Liga creada: {nuevo.id}")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al crear liga: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción (posiblemente nombre duplicado)"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear liga: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear liga"
        )


def update_liga(db: Session, liga_id: UUID, liga: LigaUpdate):
    logger.info(f"Actualizando liga {liga_id}")
    try:
        existing = get_liga(db, liga_id)
        for key, value in liga.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Liga actualizada: {liga_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al actualizar liga {liga_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar liga {liga_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar liga"
        )


def delete_liga(db: Session, liga_id: UUID):
    logger.info(f"Eliminando liga {liga_id}")
    try:
        existing = get_liga(db, liga_id)
        existing.deleted_at = datetime.now(UTC)
        existing.activo = False
        db.commit()
        db.refresh(existing)
        logger.info(f"Liga eliminada (soft delete): {liga_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al eliminar liga {liga_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: no se puede eliminar la liga (posiblemente tiene dependencias)"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar liga {liga_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar liga"
        )
