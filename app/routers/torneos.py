from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_permissions
from app.schemas.torneo import TorneoCreate, TorneoResponse, TorneoUpdate
from app.services.torneo_service import (
    create_torneo,
    delete_torneo,
    get_torneo,
    get_torneos,
    update_torneo,
)

router = APIRouter(prefix="/torneos", tags=["Torneos"])


@router.get("/", response_model=list[TorneoResponse])
def listar_torneos(db: Session = Depends(get_db)):
    return get_torneos(db)


@router.get("/{torneo_id}", response_model=TorneoResponse)
def obtener_torneo(torneo_id: UUID, db: Session = Depends(get_db)):
    torneo = get_torneo(db, torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return torneo


@router.post("/", response_model=TorneoResponse)
def crear_torneo(torneo: TorneoCreate, db: Session = Depends(get_db), _user=Depends(require_permissions("torneos:manage"))):
    return create_torneo(db, torneo)


@router.put("/{torneo_id}", response_model=TorneoResponse)
def actualizar_torneo(torneo_id: UUID, torneo: TorneoUpdate, db: Session = Depends(get_db), _user=Depends(require_permissions("torneos:manage"))):
    updated = update_torneo(db, torneo_id, torneo)
    if not updated:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return updated


@router.delete("/{torneo_id}")
def eliminar_torneo(torneo_id: UUID, db: Session = Depends(get_db), _user=Depends(require_permissions("torneos:manage"))):
    deleted = delete_torneo(db, torneo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return {"mensaje": "Torneo eliminado"}
