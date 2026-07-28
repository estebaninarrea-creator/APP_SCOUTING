from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.estadio import EstadioCreate, EstadioResponse, EstadioUpdate
from app.services.estadio_service import EstadioService

router = APIRouter(prefix="/estadios", tags=["Estadios"])


@router.get("/", response_model=list[EstadioResponse])
def listar_estadios(db: Session = Depends(get_db)):
    return EstadioService(db).get_all()


@router.get("/{estadio_id}", response_model=EstadioResponse)
def obtener_estadio(estadio_id: UUID, db: Session = Depends(get_db)):
    return EstadioService(db).get(estadio_id)


@router.post("/", response_model=EstadioResponse, status_code=status.HTTP_201_CREATED)
def crear_estadio(payload: EstadioCreate, db: Session = Depends(get_db)):
    return EstadioService(db).create(payload)


@router.put("/{estadio_id}", response_model=EstadioResponse)
def actualizar_estadio(estadio_id: UUID, payload: EstadioUpdate, db: Session = Depends(get_db)):
    return EstadioService(db).update(estadio_id, payload)


@router.delete("/{estadio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estadio(estadio_id: UUID, db: Session = Depends(get_db)):
    EstadioService(db).delete(estadio_id)
    return None
