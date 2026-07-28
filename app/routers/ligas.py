from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.liga import LigaCreate, LigaResponse, LigaUpdate
from app.services.liga_service import (
    create_liga,
    delete_liga,
    get_liga,
    get_ligas,
    update_liga,
)

router = APIRouter(prefix="/ligas", tags=["Ligas"])


@router.get("/", response_model=list[LigaResponse])
def listar_ligas(db: Session = Depends(get_db)):
    return get_ligas(db)


@router.get("/{liga_id}", response_model=LigaResponse)
def obtener_liga(liga_id: UUID, db: Session = Depends(get_db)):
    liga = get_liga(db, liga_id)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga no encontrada")
    return liga


@router.post("/", response_model=LigaResponse)
def crear_liga(liga: LigaCreate, db: Session = Depends(get_db)):
    return create_liga(db, liga)


@router.put("/{liga_id}", response_model=LigaResponse)
def actualizar_liga(liga_id: UUID, liga: LigaUpdate, db: Session = Depends(get_db)):
    updated = update_liga(db, liga_id, liga)
    if not updated:
        raise HTTPException(status_code=404, detail="Liga no encontrada")
    return updated


@router.delete("/{liga_id}")
def eliminar_liga(liga_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_liga(db, liga_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Liga no encontrada")
    return {"mensaje": "Liga eliminada"}
