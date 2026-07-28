from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.arbitro import ArbitroCreate, ArbitroResponse, ArbitroUpdate
from app.services.arbitro_service import (
    create_arbitro,
    delete_arbitro,
    get_arbitro,
    get_arbitros,
    update_arbitro,
)

router = APIRouter(prefix="/arbitros", tags=["Árbitros"])


@router.get("/", response_model=list[ArbitroResponse])
def listar_arbitros(db: Session = Depends(get_db)):
    """Lista todos los árbitros"""
    return get_arbitros(db)


@router.get("/{arbitro_id}", response_model=ArbitroResponse)
def obtener_arbitro(arbitro_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un árbitro por ID"""
    return get_arbitro(db, arbitro_id)


@router.post("/", response_model=ArbitroResponse, status_code=status.HTTP_201_CREATED)
def crear_arbitro(arbitro: ArbitroCreate, db: Session = Depends(get_db)):
    """Crea un nuevo árbitro"""
    return create_arbitro(db, arbitro)


@router.put("/{arbitro_id}", response_model=ArbitroResponse)
def actualizar_arbitro(arbitro_id: UUID, arbitro: ArbitroUpdate, db: Session = Depends(get_db)):
    """Actualiza un árbitro existente"""
    return update_arbitro(db, arbitro_id, arbitro)


@router.delete("/{arbitro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_arbitro(arbitro_id: UUID, db: Session = Depends(get_db)):
    """Elimina un árbitro"""
    delete_arbitro(db, arbitro_id)
    return None
