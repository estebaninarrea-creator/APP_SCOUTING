from typing import List
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.estado import EstadoCreate, EstadoResponse, EstadoUpdate
from app.services.estado_service import EstadoService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/estados", tags=["Estados"])


@router.get("/", response_model=List[EstadoResponse])
def listar_estados(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene lista de todos los estados de partidos con paginación
    """
    try:
        service = EstadoService(db)
        estados = service.get_all(skip=skip, limit=limit)
        logger.info(f"Listado de {len(estados)} estados")
        return estados
    except Exception as e:
        logger.error(f"Error al listar estados: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar estados"
        )


@router.get("/{estado_id}", response_model=EstadoResponse)
def obtener_estado(estado_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene un estado específico por ID
    """
    service = EstadoService(db)
    estado = service.get(estado_id)
    logger.info(f"Estado obtenido: {estado_id}")
    return estado


@router.post("/", response_model=EstadoResponse, status_code=status.HTTP_201_CREATED)
def crear_estado(estado_data: EstadoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo estado de partido
    """
    try:
        service = EstadoService(db)
        
        # Verificar que no exista un estado con ese nombre
        if service.get_by_nombre(estado_data.nombre):
            logger.warning(f"Intento de crear estado duplicado: {estado_data.nombre}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un estado con ese nombre"
            )
        
        estado = service.create(estado_data)
        logger.info(f"Estado creado: {estado.id} ({estado.nombre})")
        return estado
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al crear estado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear estado"
        )


@router.put("/{estado_id}", response_model=EstadoResponse)
def actualizar_estado(
    estado_id: UUID,
    estado_data: EstadoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un estado existente
    """
    try:
        service = EstadoService(db)
        estado = service.get(estado_id)
        
        # Si se intenta cambiar el nombre, verificar que sea único
        if estado_data.nombre and estado_data.nombre != estado.nombre:
            if service.get_by_nombre(estado_data.nombre):
                logger.warning(f"Intento de actualizar a nombre duplicado: {estado_data.nombre}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un estado con ese nombre"
                )
        
        estado = service.update(estado_id, estado_data)
        logger.info(f"Estado actualizado: {estado_id}")
        return estado
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar estado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar estado"
        )


@router.delete("/{estado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estado(estado_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un estado de partido
    """
    try:
        service = EstadoService(db)
        service.delete(estado_id)
        logger.info(f"Estado eliminado: {estado_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar estado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar estado"
        )
