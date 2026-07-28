import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.equipo import Equipos
from app.schemas.equipo import EquipoCreate, EquipoUpdate

logger = logging.getLogger(__name__)


def get_equipos(db: Session):
    logger.info("Obteniendo todos los equipos")
    try:
        result = db.query(Equipos).order_by(Equipos.nombre).all()
        logger.info(f"Se obtuvieron {len(result)} equipos")
        return result
    except Exception as e:
        logger.error(f"Error al obtener equipos: {str(e)}")
        raise


def get_equipo(db: Session, equipo_id: UUID):
    logger.info(f"Obteniendo equipo {equipo_id}")
    try:
        result = db.query(Equipos).filter(Equipos.id == equipo_id).first()
        if not result:
            logger.warning(f"Equipo no encontrado: {equipo_id}")
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener equipo {equipo_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener equipo")


def create_equipo(db: Session, equipo: EquipoCreate):
    logger.info(f"Creando nuevo equipo")
    try:
        nuevo = Equipos(**equipo.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Equipo creado: {nuevo.id}")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: violación de restricción")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear equipo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear equipo")


def update_equipo(db: Session, equipo_id: UUID, equipo: EquipoUpdate):
    logger.info(f"Actualizando equipo {equipo_id}")
    try:
        existing = get_equipo(db, equipo_id)
        for key, value in equipo.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Equipo actualizado: {equipo_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: violación de restricción")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar equipo {equipo_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar equipo")


def delete_equipo(db: Session, equipo_id: UUID):
    logger.info(f"Eliminando equipo {equipo_id}")
    try:
        existing = get_equipo(db, equipo_id)
        db.delete(existing)
        db.commit()
        logger.info(f"Equipo eliminado: {equipo_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="No se puede eliminar el equipo")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar equipo {equipo_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar equipo")
