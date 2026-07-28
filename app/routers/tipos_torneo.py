from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.tipo_torneo import TipoTorneoCreate, TipoTorneoResponse, TipoTorneoUpdate
from app.services.tipo_torneo_service import (
    create_tipo_torneo,
    delete_tipo_torneo,
    get_tipo_torneo,
    get_tipos_torneo,
    update_tipo_torneo,
)

router = APIRouter(prefix="/tipos_torneo", tags=["Tipos de torneo"])


@router.get("/", response_model=list[TipoTorneoResponse])
def listar_tipos_torneo(db: Session = Depends(get_db)):
    """Lista todos los tipos de torneo"""
    return get_tipos_torneo(db)


@router.get("/{tipo_torneo_id}", response_model=TipoTorneoResponse)
def obtener_tipo_torneo(tipo_torneo_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un tipo de torneo por ID"""
    return get_tipo_torneo(db, tipo_torneo_id)


@router.post("/", response_model=TipoTorneoResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_torneo(tipo_torneo: TipoTorneoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo tipo de torneo"""
    return create_tipo_torneo(db, tipo_torneo)


@router.put("/{tipo_torneo_id}", response_model=TipoTorneoResponse)
def actualizar_tipo_torneo(tipo_torneo_id: UUID, tipo_torneo: TipoTorneoUpdate, db: Session = Depends(get_db)):
    """Actualiza un tipo de torneo existente"""
    return update_tipo_torneo(db, tipo_torneo_id, tipo_torneo)


@router.delete("/{tipo_torneo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_torneo(tipo_torneo_id: UUID, db: Session = Depends(get_db)):
    """Elimina un tipo de torneo"""
    delete_tipo_torneo(db, tipo_torneo_id)
    return None
