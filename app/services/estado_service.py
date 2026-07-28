from typing import Optional
from uuid import UUID
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

from app.models import Estados
from app.schemas.estado import EstadoCreate, EstadoUpdate
from app.services.crud_service import CRUDService

logger = logging.getLogger(__name__)


class EstadoService(CRUDService[Estados, EstadoCreate, EstadoUpdate]):
    """
    Service para gestionar Estados de partidos
    """
    
    def __init__(self, db: Session):
        super().__init__(db, Estados)
    
    def get_by_nombre(self, nombre: str) -> Optional[Estados]:
        """Obtiene un estado por su nombre"""
        try:
            return self.db.query(Estados).filter(
                Estados.nombre == nombre
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener estado por nombre '{nombre}': {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al consultar estados"
            )
