from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.scout import ScoutCreate, ScoutResponse, ScoutUpdate
from app.services.scout_service import (
    create_scout,
    delete_scout,
    get_scout,
    get_scouts,
    update_scout,
)

router = APIRouter(prefix="/scouts", tags=["Scouts"])


@router.get("/", response_model=list[ScoutResponse])
def listar_scouts(db: Session = Depends(get_db)):
    return get_scouts(db)


@router.get("/{scout_id}", response_model=ScoutResponse)
def obtener_scout(scout_id: UUID, db: Session = Depends(get_db)):
    scout = get_scout(db, scout_id)
    if not scout:
        raise HTTPException(status_code=404, detail="Scout no encontrado")
    return scout


@router.post("/", response_model=ScoutResponse)
def crear_scout(scout: ScoutCreate, db: Session = Depends(get_db)):
    return create_scout(db, scout)


@router.put("/{scout_id}", response_model=ScoutResponse)
def actualizar_scout(scout_id: UUID, scout: ScoutUpdate, db: Session = Depends(get_db)):
    updated = update_scout(db, scout_id, scout)
    if not updated:
        raise HTTPException(status_code=404, detail="Scout no encontrado")
    return updated


@router.delete("/{scout_id}")
def eliminar_scout(scout_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_scout(db, scout_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scout no encontrado")
    return {"mensaje": "Scout eliminado"}
