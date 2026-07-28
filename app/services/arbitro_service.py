from uuid import UUID
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

from app.models.arbitro import Arbitros
from app.schemas.arbitro import ArbitroCreate, ArbitroUpdate

logger = logging.getLogger(__name__)


def get_arbitros(db: Session):
    """Obtiene todos los árbitros"""
    logger.info("Obteniendo todos los árbitros")
    try:
        result = db.query(Arbitros).order_by(Arbitros.apellido, Arbitros.nombre).all()
        logger.info(f"Se obtuvieron {len(result)} árbitros")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener árbitros: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener árbitros"
        )


def get_arbitro(db: Session, arbitro_id: UUID):
    """Obtiene un árbitro por ID"""
    logger.info(f"Obteniendo árbitro {arbitro_id}")
    try:
        arbitro = db.query(Arbitros).filter(Arbitros.id == arbitro_id).first()
        if not arbitro:
            logger.warning(f"Árbitro no encontrado: {arbitro_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Árbitro no encontrado"
            )
        logger.info(f"Árbitro encontrado: {arbitro_id}")
        return arbitro
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener árbitro {arbitro_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener árbitro"
        )


def create_arbitro(db: Session, arbitro: ArbitroCreate):
    """Crea un nuevo árbitro"""
    logger.info(f"Creando nuevo árbitro")
    try:
        nuevo = Arbitros(**arbitro.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Árbitro creado: {nuevo.id} ({nuevo.nombre} {nuevo.apellido})")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al crear árbitro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción (posiblemente FK inválido)"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear árbitro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear árbitro"
        )


def update_arbitro(db: Session, arbitro_id: UUID, arbitro: ArbitroUpdate):
    """Actualiza un árbitro existente"""
    logger.info(f"Actualizando árbitro {arbitro_id}")
    try:
        existing = get_arbitro(db, arbitro_id)
        for key, value in arbitro.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Árbitro actualizado: {arbitro_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al actualizar árbitro {arbitro_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar árbitro {arbitro_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar árbitro"
        )


def delete_arbitro(db: Session, arbitro_id: UUID):
    """Elimina un árbitro"""
    logger.info(f"Eliminando árbitro {arbitro_id}")
    try:
        existing = get_arbitro(db, arbitro_id)
        db.delete(existing)
        db.commit()
        logger.info(f"Árbitro eliminado: {arbitro_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al eliminar árbitro {arbitro_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: no se puede eliminar el árbitro (posiblemente tiene dependencias)"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar árbitro {arbitro_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar árbitro"
        )
