from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.cancha import CanchaCreate, CanchaResponse, CanchaUpdate
from app.services.cancha_service import CanchaService

router = APIRouter(prefix="/canchas", tags=["Canchas"])


@router.get("/", response_model=list[CanchaResponse])
def listar_canchas(db: Session = Depends(get_db)):
    return CanchaService(db).get_all()


@router.get("/{cancha_id}", response_model=CanchaResponse)
def obtener_cancha(cancha_id: UUID, db: Session = Depends(get_db)):
    return CanchaService(db).get(cancha_id)


@router.post("/", response_model=CanchaResponse, status_code=status.HTTP_201_CREATED)
def crear_cancha(payload: CanchaCreate, db: Session = Depends(get_db)):
    return CanchaService(db).create(payload)


@router.put("/{cancha_id}", response_model=CanchaResponse)
def actualizar_cancha(cancha_id: UUID, payload: CanchaUpdate, db: Session = Depends(get_db)):
    return CanchaService(db).update(cancha_id, payload)


@router.delete("/{cancha_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cancha(cancha_id: UUID, db: Session = Depends(get_db)):
    CanchaService(db).delete(cancha_id)
    return None
