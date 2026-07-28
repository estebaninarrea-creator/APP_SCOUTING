from typing import Generic, TypeVar
from uuid import UUID
import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logger = logging.getLogger(__name__)

ModelT = TypeVar("ModelT")
CreateT = TypeVar("CreateT")
UpdateT = TypeVar("UpdateT")


class CRUDService(Generic[ModelT, CreateT, UpdateT]):
    def __init__(self, db: Session, model_cls):
        self.db = db
        self.model_cls = model_cls

    def get_all(self, *, order_by=None, skip: int = 0, limit: int = 100):
        """Obtiene todos los registros con paginación opcional"""
        try:
            query = self.db.query(self.model_cls)
            if order_by is not None:
                query = query.order_by(order_by)
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener registros: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al obtener datos de la base de datos"
            )

    def get(self, item_id: UUID):
        """Obtiene un registro por ID"""
        try:
            item = self.db.query(self.model_cls).filter(
                self.model_cls.id == item_id
            ).first()
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro no encontrado"
                )
            return item
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener registro {item_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al obtener registro"
            )

    def create(self, data: CreateT):
        """Crea un nuevo registro"""
        try:
            obj = self.model_cls(**data.model_dump(exclude_unset=True))
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            logger.info(f"Registro creado: {obj.id}")
            return obj
        except IntegrityError as e:
            self.db.rollback()
            logger.warning(f"Error de integridad al crear: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: violación de restricción de base de datos (posiblemente duplicado)"
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error al crear registro: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear registro en la base de datos"
            )

    def update(self, item_id: UUID, data: UpdateT):
        """Actualiza un registro existente"""
        try:
            item = self.get(item_id)
            for key, value in data.model_dump(exclude_unset=True).items():
                if value is not None:
                    setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            logger.info(f"Registro actualizado: {item_id}")
            return item
        except HTTPException:
            raise
        except IntegrityError as e:
            self.db.rollback()
            logger.warning(f"Error de integridad al actualizar {item_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: violación de restricción de base de datos"
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error al actualizar registro {item_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar registro"
            )

    def delete(self, item_id: UUID):
        """Elimina un registro"""
        try:
            item = self.get(item_id)
            self.db.delete(item)
            self.db.commit()
            logger.info(f"Registro eliminado: {item_id}")
            return item
        except HTTPException:
            raise
        except IntegrityError as e:
            self.db.rollback()
            logger.warning(f"Error de integridad al eliminar {item_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar: existen registros relacionados"
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error al eliminar registro {item_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar registro"
            )
