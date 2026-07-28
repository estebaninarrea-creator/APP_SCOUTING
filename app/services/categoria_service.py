import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.categoria import Categorias
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate

logger = logging.getLogger(__name__)


def get_categorias(db: Session) -> list[Categorias]:
    """Obtiene todas las categorías"""
    logger.info("Obteniendo todas las categorías")
    try:
        return db.query(Categorias).order_by(Categorias.nombre).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener categorías: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener categorías")


def get_categoria(db: Session, categoria_id: UUID) -> Categorias:
    """Obtiene una categoría por ID"""
    logger.info(f"Obteniendo categoría {categoria_id}")
    try:
        categoria = db.query(Categorias).filter(Categorias.id == categoria_id).first()
        if not categoria:
            logger.warning(f"Categoría {categoria_id} no encontrada")
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return categoria
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener categoría")


def create_categoria(db: Session, categoria: CategoriaCreate) -> Categorias:
    """Crea una nueva categoría"""
    logger.info(f"Creando categoría: {categoria.nombre}")
    try:
        db_categoria = Categorias(**categoria.model_dump())
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        logger.info(f"Categoría creada: {db_categoria.id}")
        return db_categoria
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="El nombre de la categoría ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear categoría")


def update_categoria(db: Session, categoria_id: UUID, categoria: CategoriaUpdate) -> Categorias:
    """Actualiza una categoría existente"""
    logger.info(f"Actualizando categoría {categoria_id}")
    try:
        db_categoria = db.query(Categorias).filter(Categorias.id == categoria_id).first()
        if not db_categoria:
            logger.warning(f"Categoría {categoria_id} no encontrada")
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        
        update_data = categoria.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_categoria, key, value)
        
        db.commit()
        db.refresh(db_categoria)
        logger.info(f"Categoría actualizada: {db_categoria.id}")
        return db_categoria
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="El nombre de la categoría ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar categoría")


def delete_categoria(db: Session, categoria_id: UUID) -> None:
    """Elimina una categoría"""
    logger.info(f"Eliminando categoría {categoria_id}")
    try:
        db_categoria = db.query(Categorias).filter(Categorias.id == categoria_id).first()
        if not db_categoria:
            logger.warning(f"Categoría {categoria_id} no encontrada")
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        
        db.delete(db_categoria)
        db.commit()
        logger.info(f"Categoría eliminada: {db_categoria.id}")
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="No se puede eliminar la categoría: tiene equipos o torneos asociados")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar categoría")
