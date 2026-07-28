from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.formacion_jugador import (
    FormacionJugadorCreate,
    FormacionJugadorResponse,
    FormacionJugadorUpdate,
)
from app.services.formacion_jugador_service import FormacionJugadorService

router = APIRouter(prefix="/formacion_jugadores", tags=["Formación Jugadores"])


@router.get("/", response_model=list[FormacionJugadorResponse])
def listar_formacion_jugadores(db: Session = Depends(get_db)):
    return FormacionJugadorService(db).get_all()


@router.get("/{formacion_jugador_id}", response_model=FormacionJugadorResponse)
def obtener_formacion_jugador(formacion_jugador_id: UUID, db: Session = Depends(get_db)):
    return FormacionJugadorService(db).get(formacion_jugador_id)


@router.post("/", response_model=FormacionJugadorResponse, status_code=status.HTTP_201_CREATED)
def crear_formacion_jugador(payload: FormacionJugadorCreate, db: Session = Depends(get_db)):
    return FormacionJugadorService(db).create(payload)


@router.put("/{formacion_jugador_id}", response_model=FormacionJugadorResponse)
def actualizar_formacion_jugador(formacion_jugador_id: UUID, payload: FormacionJugadorUpdate, db: Session = Depends(get_db)):
    return FormacionJugadorService(db).update(formacion_jugador_id, payload)


@router.delete("/{formacion_jugador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_formacion_jugador(formacion_jugador_id: UUID, db: Session = Depends(get_db)):
    FormacionJugadorService(db).delete(formacion_jugador_id)
    return None
