import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.scout import Scouts
from app.schemas.scout import ScoutCreate, ScoutUpdate

logger = logging.getLogger(__name__)


def get_scouts(db: Session):
    logger.info("Obteniendo todos los scouts")
    try:
        result = db.query(Scouts).order_by(Scouts.apellido, Scouts.nombre).all()
        logger.info(f"Se obtuvieron {len(result)} scouts")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener scouts: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener scouts")


def get_scout(db: Session, scout_id: UUID):
    logger.info(f"Obteniendo scout {scout_id}")
    try:
        result = db.query(Scouts).filter(Scouts.id == scout_id).first()
        if not result:
            logger.warning(f"Scout no encontrado: {scout_id}")
            raise HTTPException(status_code=404, detail="Scout no encontrado")
        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener scout {scout_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener scout")


def create_scout(db: Session, scout: ScoutCreate):
    logger.info(f"Creando nuevo scout")
    try:
        nuevo = Scouts(**scout.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Scout creado: {nuevo.id}")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: violación de restricción")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear scout: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear scout")


def update_scout(db: Session, scout_id: UUID, scout: ScoutUpdate):
    logger.info(f"Actualizando scout {scout_id}")
    try:
        existing = get_scout(db, scout_id)
        for key, value in scout.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Scout actualizado: {scout_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: violación de restricción")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar scout {scout_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar scout")


def delete_scout(db: Session, scout_id: UUID):
    logger.info(f"Eliminando scout {scout_id}")
    try:
        existing = get_scout(db, scout_id)
        if existing:
            db.delete(existing)
            db.commit()
            logger.info(f"Scout eliminado: {scout_id}")
        else:
            logger.warning(f"Scout no encontrado para eliminar: {scout_id}")
        return existing
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar scout {scout_id}: {str(e)}")
        raise
