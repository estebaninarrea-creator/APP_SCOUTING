import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.tipo_torneo import TiposTorneo
from app.schemas.tipo_torneo import TipoTorneoCreate, TipoTorneoUpdate

logger = logging.getLogger(__name__)


def get_tipos_torneo(db: Session) -> list[TiposTorneo]:
    """Obtiene todos los tipos de torneo"""
    logger.info("Obteniendo todos los tipos de torneo")
    try:
        return db.query(TiposTorneo).order_by(TiposTorneo.nombre).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener tipos de torneo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener tipos de torneo")


def get_tipo_torneo(db: Session, tipo_torneo_id: UUID) -> TiposTorneo:
    """Obtiene un tipo de torneo por ID"""
    logger.info(f"Obteniendo tipo de torneo {tipo_torneo_id}")
    try:
        tipo = db.query(TiposTorneo).filter(TiposTorneo.id == tipo_torneo_id).first()
        if not tipo:
            logger.warning(f"Tipo de torneo {tipo_torneo_id} no encontrado")
            raise HTTPException(status_code=404, detail="Tipo de torneo no encontrado")
        return tipo
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener tipo de torneo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener tipo de torneo")


def create_tipo_torneo(db: Session, tipo_torneo: TipoTorneoCreate) -> TiposTorneo:
    """Crea un nuevo tipo de torneo"""
    logger.info(f"Creando tipo de torneo: {tipo_torneo.nombre}")
    try:
        db_tipo = TiposTorneo(**tipo_torneo.model_dump())
        db.add(db_tipo)
        db.commit()
        db.refresh(db_tipo)
        logger.info(f"Tipo de torneo creado: {db_tipo.id}")
        return db_tipo
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="El nombre del tipo de torneo ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear tipo de torneo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear tipo de torneo")


def update_tipo_torneo(db: Session, tipo_torneo_id: UUID, tipo_torneo: TipoTorneoUpdate) -> TiposTorneo:
    """Actualiza un tipo de torneo existente"""
    logger.info(f"Actualizando tipo de torneo {tipo_torneo_id}")
    try:
        db_tipo = db.query(TiposTorneo).filter(TiposTorneo.id == tipo_torneo_id).first()
        if not db_tipo:
            logger.warning(f"Tipo de torneo {tipo_torneo_id} no encontrado")
            raise HTTPException(status_code=404, detail="Tipo de torneo no encontrado")
        
        update_data = tipo_torneo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tipo, key, value)
        
        db.commit()
        db.refresh(db_tipo)
        logger.info(f"Tipo de torneo actualizado: {db_tipo.id}")
        return db_tipo
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="El nombre del tipo de torneo ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar tipo de torneo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar tipo de torneo")


def delete_tipo_torneo(db: Session, tipo_torneo_id: UUID) -> None:
    """Elimina un tipo de torneo"""
    logger.info(f"Eliminando tipo de torneo {tipo_torneo_id}")
    try:
        db_tipo = db.query(TiposTorneo).filter(TiposTorneo.id == tipo_torneo_id).first()
        if not db_tipo:
            logger.warning(f"Tipo de torneo {tipo_torneo_id} no encontrado")
            raise HTTPException(status_code=404, detail="Tipo de torneo no encontrado")
        
        db.delete(db_tipo)
        db.commit()
        logger.info(f"Tipo de torneo eliminado: {db_tipo.id}")
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="No se puede eliminar el tipo de torneo: tiene torneos asociados")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar tipo de torneo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar tipo de torneo")
