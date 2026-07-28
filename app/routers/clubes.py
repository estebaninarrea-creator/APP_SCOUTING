from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.club import ClubCreate, ClubResponse, ClubUpdate
from app.services.club_service import (
    create_club,
    delete_club,
    get_club,
    get_clubes,
    update_club,
)

router = APIRouter(prefix="/clubes", tags=["Clubes"])


@router.get("/", response_model=list[ClubResponse])
def listar_clubes(db: Session = Depends(get_db)):
    return get_clubes(db)


@router.get("/{club_id}", response_model=ClubResponse)
def obtener_club(club_id: UUID, db: Session = Depends(get_db)):
    club = get_club(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return club


@router.post("/", response_model=ClubResponse)
def crear_club(club: ClubCreate, db: Session = Depends(get_db)):
    return create_club(db, club)


@router.put("/{club_id}", response_model=ClubResponse)
def actualizar_club(club_id: UUID, club: ClubUpdate, db: Session = Depends(get_db)):
    updated = update_club(db, club_id, club)
    if not updated:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return updated


@router.delete("/{club_id}")
def eliminar_club(club_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = delete_club(db, club_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    if not deleted:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return {"mensaje": "Club eliminado"}
