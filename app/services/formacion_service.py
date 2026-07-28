import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.formacion import Formaciones
from app.schemas.formacion import FormacionCreate, FormacionUpdate

logger = logging.getLogger(__name__)


def get_formaciones(db: Session) -> list[Formaciones]:
    """Obtiene todas las formaciones"""
    logger.info("Obteniendo todas las formaciones")
    try:
        return db.query(Formaciones).order_by(Formaciones.created_at.desc()).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener formaciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener formaciones")


def get_formacion(db: Session, formacion_id: UUID) -> Formaciones:
    """Obtiene una formación por ID"""
    logger.info(f"Obteniendo formación {formacion_id}")
    try:
        formacion = db.query(Formaciones).filter(Formaciones.id == formacion_id).first()
        if not formacion:
            logger.warning(f"Formación {formacion_id} no encontrada")
            raise HTTPException(status_code=404, detail="Formación no encontrada")
        return formacion
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener formación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener formación")


def create_formacion(db: Session, formacion: FormacionCreate) -> Formaciones:
    """Crea una nueva formación"""
    logger.info(f"Creando formación para partido {formacion.partido_id}, equipo {formacion.equipo_id}")
    try:
        db_formacion = Formaciones(**formacion.model_dump())
        db.add(db_formacion)
        db.commit()
        db.refresh(db_formacion)
        logger.info(f"Formación creada: {db_formacion.id}")
        return db_formacion
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: partido o equipo no existen")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear formación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear formación")


def update_formacion(db: Session, formacion_id: UUID, formacion: FormacionUpdate) -> Formaciones:
    """Actualiza una formación existente"""
    logger.info(f"Actualizando formación {formacion_id}")
    try:
        db_formacion = db.query(Formaciones).filter(Formaciones.id == formacion_id).first()
        if not db_formacion:
            logger.warning(f"Formación {formacion_id} no encontrada")
            raise HTTPException(status_code=404, detail="Formación no encontrada")
        
        update_data = formacion.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_formacion, key, value)
        
        db.commit()
        db.refresh(db_formacion)
        logger.info(f"Formación actualizada: {db_formacion.id}")
        return db_formacion
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: partido o equipo no existen")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar formación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar formación")


def delete_formacion(db: Session, formacion_id: UUID) -> None:
    """Elimina una formación"""
    logger.info(f"Eliminando formación {formacion_id}")
    try:
        db_formacion = db.query(Formaciones).filter(Formaciones.id == formacion_id).first()
        if not db_formacion:
            logger.warning(f"Formación {formacion_id} no encontrada")
            raise HTTPException(status_code=404, detail="Formación no encontrada")
        
        db.delete(db_formacion)
        db.commit()
        logger.info(f"Formación eliminada: {db_formacion.id}")
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="No se puede eliminar la formación")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar formación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar formación")
