from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.torneo_club import TorneoClubCreate, TorneoClubResponse, TorneoClubUpdate
from app.services.torneo_club_service import TorneoClubService

router = APIRouter(prefix="/torneos_clubes", tags=["Torneos-Clubes"])


@router.get("/", response_model=list[TorneoClubResponse])
def listar_torneos_clubes(db: Session = Depends(get_db)):
    return TorneoClubService(db).get_all()


@router.get("/{torneo_id}/{equipo_id}", response_model=TorneoClubResponse)
def obtener_torneo_club(torneo_id: UUID, equipo_id: UUID, db: Session = Depends(get_db)):
    return TorneoClubService(db).get(torneo_id, equipo_id)


@router.post("/", response_model=TorneoClubResponse, status_code=status.HTTP_201_CREATED)
def crear_torneo_club(payload: TorneoClubCreate, db: Session = Depends(get_db)):
    return TorneoClubService(db).create(payload)


@router.put("/{torneo_id}/{equipo_id}", response_model=TorneoClubResponse)
def actualizar_torneo_club(torneo_id: UUID, equipo_id: UUID, payload: TorneoClubUpdate, db: Session = Depends(get_db)):
    return TorneoClubService(db).update(torneo_id, equipo_id, payload)


@router.delete("/{torneo_id}/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_torneo_club(torneo_id: UUID, equipo_id: UUID, db: Session = Depends(get_db)):
    TorneoClubService(db).delete(torneo_id, equipo_id)
    return None
