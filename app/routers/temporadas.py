from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.temporada import TemporadaCreate, TemporadaResponse, TemporadaUpdate
from app.services.temporada_service import (
    create_temporada,
    delete_temporada,
    get_temporada,
    get_temporadas,
    update_temporada,
)

router = APIRouter(prefix="/temporadas", tags=["Temporadas"])


@router.get("/", response_model=list[TemporadaResponse])
def listar_temporadas(db: Session = Depends(get_db)):
    return get_temporadas(db)


@router.get("/{temporada_id}", response_model=TemporadaResponse)
def obtener_temporada(temporada_id: UUID, db: Session = Depends(get_db)):
    temporada = get_temporada(db, temporada_id)
    if not temporada:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return temporada


@router.post("/", response_model=TemporadaResponse)
def crear_temporada(temporada: TemporadaCreate, db: Session = Depends(get_db)):
    return create_temporada(db, temporada)


@router.put("/{temporada_id}", response_model=TemporadaResponse)
def actualizar_temporada(temporada_id: UUID, temporada: TemporadaUpdate, db: Session = Depends(get_db)):
    updated = update_temporada(db, temporada_id, temporada)
    if not updated:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return updated


@router.delete("/{temporada_id}")
def eliminar_temporada(temporada_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_temporada(db, temporada_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return {"mensaje": "Temporada eliminada"}
