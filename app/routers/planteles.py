from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_permissions
from app.schemas.plantel import PlantelCreate, PlantelResponse, PlantelUpdate
from app.services.plantel_service import (
    create_plantel,
    delete_plantel,
    get_plantel,
    get_planteles,
    update_plantel,
)

router = APIRouter(prefix="/planteles", tags=["Planteles"])


@router.get("/", response_model=list[PlantelResponse])
def listar_planteles(
    equipo_id: UUID | None = None,
    temporada_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    """Lista planteles, opcionalmente filtrados por equipo y temporada"""
    return get_planteles(db, equipo_id=equipo_id, temporada_id=temporada_id)


@router.get("/{plantel_id}", response_model=PlantelResponse)
def obtener_plantel(plantel_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un plantel por ID"""
    return get_plantel(db, plantel_id)


@router.post("/", response_model=PlantelResponse, status_code=status.HTTP_201_CREATED)
def crear_plantel(plantel: PlantelCreate, db: Session = Depends(get_db), _user=Depends(require_permissions("planteles:manage"))):
    """Crea un nuevo plantel"""
    return create_plantel(db, plantel)


@router.put("/{plantel_id}", response_model=PlantelResponse)
def actualizar_plantel(plantel_id: UUID, plantel: PlantelUpdate, db: Session = Depends(get_db), _user=Depends(require_permissions("planteles:manage"))):
    """Actualiza un plantel existente"""
    return update_plantel(db, plantel_id, plantel)


@router.delete("/{plantel_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_plantel(plantel_id: UUID, db: Session = Depends(get_db), _user=Depends(require_permissions("planteles:manage"))):
    """Elimina un plantel"""
    delete_plantel(db, plantel_id)
    return None
