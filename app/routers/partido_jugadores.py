from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_permissions
from app.schemas.partido_jugador import PartidoJugadorCreate, PartidoJugadorResponse, PartidoJugadorUpdate
from app.services.partido_jugador_service import (
    create_partido_jugador,
    delete_partido_jugador,
    get_partido_jugadores,
    update_partido_jugador,
)

router = APIRouter(prefix="/partidos/{partido_id}/jugadores", tags=["PartidoJugadores"])


@router.get("/", response_model=list[PartidoJugadorResponse])
def listar_partido_jugadores(partido_id: UUID, db: Session = Depends(get_db)):
    return get_partido_jugadores(db, partido_id)


@router.post("/", response_model=PartidoJugadorResponse, status_code=status.HTTP_201_CREATED)
def crear_partido_jugador(partido_id: UUID, payload: PartidoJugadorCreate, db: Session = Depends(get_db), _user=Depends(require_permissions("partido_jugadores:manage"))):
    return create_partido_jugador(db, partido_id, payload)


@router.put("/{partido_jugador_id}", response_model=PartidoJugadorResponse)
def actualizar_partido_jugador(partido_id: UUID, partido_jugador_id: UUID, payload: PartidoJugadorUpdate, db: Session = Depends(get_db), _user=Depends(require_permissions("partido_jugadores:manage"))):
    return update_partido_jugador(db, partido_id, partido_jugador_id, payload)


@router.delete("/{partido_jugador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_partido_jugador(partido_id: UUID, partido_jugador_id: UUID, db: Session = Depends(get_db), _user=Depends(require_permissions("partido_jugadores:manage"))):
    delete_partido_jugador(db, partido_id, partido_jugador_id)
    return None
