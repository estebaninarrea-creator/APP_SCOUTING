from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_permissions
from app.schemas.equipo import EquipoCreate, EquipoResponse, EquipoUpdate
from app.services.equipo_service import (
    create_equipo,
    delete_equipo,
    get_equipo,
    get_equipos,
    update_equipo,
)

router = APIRouter(prefix="/equipos", tags=["Equipos"])


@router.get("/", response_model=list[EquipoResponse])
def listar_equipos(db: Session = Depends(get_db)):
    return get_equipos(db)


@router.get("/{equipo_id}", response_model=EquipoResponse)
def obtener_equipo(equipo_id: UUID, db: Session = Depends(get_db)):
    equipo = get_equipo(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo


@router.post("/", response_model=EquipoResponse)
def crear_equipo(equipo: EquipoCreate, db: Session = Depends(get_db), _user=Depends(require_permissions("equipos:manage"))):
    return create_equipo(db, equipo)


@router.put("/{equipo_id}", response_model=EquipoResponse)
def actualizar_equipo(equipo_id: UUID, equipo: EquipoUpdate, db: Session = Depends(get_db), _user=Depends(require_permissions("equipos:manage"))):
    updated = update_equipo(db, equipo_id, equipo)
    if not updated:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return updated


@router.delete("/{equipo_id}")
def eliminar_equipo(equipo_id: UUID, db: Session = Depends(get_db), _user=Depends(require_permissions("equipos:manage"))):
    deleted = delete_equipo(db, equipo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"mensaje": "Equipo eliminado"}
