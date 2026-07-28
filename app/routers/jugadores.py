from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.usuario import Usuarios
from app.schemas.jugador import (
    JugadorCreate,
    JugadorResponse,
    JugadorUpdate,
)

from app.services.jugador_service import (
    get_jugadores,
    get_jugador,
    create_jugador,
    update_jugador,
    delete_jugador,
)


router = APIRouter(
    prefix="/jugadores",
    tags=["Jugadores"],
)


# =========================
# LISTAR JUGADORES
# =========================

@router.get(
    "/",
    response_model=list[JugadorResponse]
)
def listar_jugadores(
    db: Session = Depends(get_db)
):
    return get_jugadores(db)


# =========================
# OBTENER JUGADOR POR ID
# =========================

@router.get(
    "/{jugador_id}",
    response_model=JugadorResponse
)
def obtener_jugador(
    jugador_id: UUID,
    db: Session = Depends(get_db)
):
    jugador = get_jugador(db, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


# =========================
# CREAR JUGADOR (Requiere autenticación)
# =========================

@router.post(
    "/",
    response_model=JugadorResponse
)
def crear_jugador(
    jugador: JugadorCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    """Crea un nuevo jugador. Requiere token JWT."""
    return create_jugador(db, jugador)


@router.put(
    "/{jugador_id}",
    response_model=JugadorResponse
)
def actualizar_jugador(
    jugador_id: UUID,
    jugador: JugadorUpdate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    """Actualiza un jugador. Requiere token JWT."""
    updated = update_jugador(db, jugador_id, jugador)
    if not updated:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return updated


@router.delete("/{jugador_id}")
def eliminar_jugador(
    jugador_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    """Elimina un jugador. Requiere token JWT."""
    deleted = delete_jugador(db, jugador_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"mensaje": "Jugador eliminado"}
