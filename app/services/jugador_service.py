from uuid import UUID
import logging

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

from app.models.jugador import Jugadores
from app.models.jugador_posicion import JugadoresPosiciones
from app.models.posicion import Posiciones
from app.schemas.jugador import JugadorCreate, JugadorUpdate

logger = logging.getLogger(__name__)


def normalize_pierna_habil(value: str | None) -> str | None:
    if value is None:
        return None

    if isinstance(value, str):
        normalized = value.strip().lower()
    else:
        normalized = str(value).strip().lower()

    mapping = {
        "d": "D",
        "derecha": "D",
        "right": "D",
        "i": "I",
        "izquierda": "I",
        "left": "I",
        "a": "A",
        "ambas": "A",
        "both": "A",
    }

    if len(str(value).strip()) > 1 and normalized not in mapping:
        return None

    if normalized in mapping:
        return mapping[normalized]
    if normalized in {"d", "i", "a"}:
        return normalized.upper()
    return None


# =========================
# LISTAR
# =========================

def get_jugadores(db: Session):
    """Obtiene todos los jugadores"""
    try:
        return (
            db.query(Jugadores)
            .order_by(
                Jugadores.apellido,
                Jugadores.nombre
            )
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugadores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener jugadores"
        )



# =========================
# BUSCAR POR ID
# =========================

def get_jugador(
    db: Session,
    jugador_id: UUID
):
    """Obtiene un jugador por ID"""
    try:
        jugador = (
            db.query(Jugadores)
            .filter(
                Jugadores.id == jugador_id
            )
            .first()
        )
        if not jugador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jugador no encontrado"
            )
        return jugador
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener jugador {jugador_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener jugador"
        )



# =========================
# CREAR
# =========================

def _sync_posiciones_jugador(db: Session, jugador_db: Jugadores, posiciones_payload):
    if posiciones_payload is None:
        return

    existing = db.query(JugadoresPosiciones).filter(JugadoresPosiciones.jugador_id == jugador_db.id).all()
    for row in existing:
        db.delete(row)

    for item in posiciones_payload:
        if isinstance(item, dict):
            posicion_id = item.get("id")
            principal = item.get("principal", False)
        else:
            posicion_id = getattr(item, "id", None)
            principal = getattr(item, "principal", False)

        if not posicion_id:
            continue

        posicion_db = db.query(Posiciones).filter(Posiciones.id == posicion_id).first()
        if not posicion_db:
            continue

        db.add(
            JugadoresPosiciones(
                jugador_id=jugador_db.id,
                posicion_id=posicion_id,
                principal=principal,
            )
        )


def create_jugador(
    db: Session,
    jugador: JugadorCreate
):
    """Crea un nuevo jugador"""
    try:
        nuevo = Jugadores(
            apellido=jugador.apellido,
            nombre=jugador.nombre,

            comet_id=jugador.comet_id,
            documento=jugador.documento,

            fecha_nacimiento=jugador.fecha_nacimiento,

            pais_id=jugador.pais_id,
            ciudad_id=jugador.ciudad_id,

            altura=jugador.altura,
            peso=jugador.peso,

            pierna_habil=normalize_pierna_habil(jugador.pierna_habil),

            foto_url=jugador.foto_url,

            activo=jugador.activo if jugador.activo is not None else True
        )


        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        _sync_posiciones_jugador(db, nuevo, jugador.posiciones)
        db.commit()
        db.refresh(nuevo)

        logger.info(f"Jugador creado: {nuevo.id} ({nuevo.nombre} {nuevo.apellido})")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al crear jugador: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción de base de datos (posiblemente documento duplicado)"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear jugador: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear jugador"
        )


def update_jugador(
    db: Session,
    jugador_id: UUID,
    jugador: JugadorUpdate
):
    """Actualiza un jugador existente"""
    try:
        existing = get_jugador(db, jugador_id)

        payload = jugador.model_dump(exclude_unset=True)

        for key, value in payload.items():
            if key == "pierna_habil":
                value = normalize_pierna_habil(value)
            if key == "posiciones":
                continue
            if value is not None:
                setattr(existing, key, value)

        if "posiciones" in payload:
            _sync_posiciones_jugador(db, existing, payload["posiciones"])

        db.commit()
        db.refresh(existing)

        logger.info(f"Jugador actualizado: {jugador_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al actualizar jugador {jugador_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción de base de datos"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar jugador {jugador_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar jugador"
        )


def delete_jugador(db: Session, jugador_id: UUID):
    """
    Elimina un jugador. Intenta borrado duro primero, si falla,
    realiza soft delete (marcándolo como inactivo).
    
    Args:
        db: Sesión de la base de datos
        jugador_id: ID del jugador a eliminar
        
    Returns:
        El jugador eliminado o None si no existe
        
    Raises:
        HTTPException: Si hay error en la operación
    """
    try:
        existing = get_jugador(db, jugador_id)

        try:
            # Intenta borrado duro
            db.delete(existing)
            db.commit()
            logger.info(f"Jugador eliminado (hard delete): {jugador_id}")
            return existing
        except IntegrityError:
            db.rollback()
            try:
                # Si falla, re-query y realiza soft delete
                existing = db.query(Jugadores).filter(Jugadores.id == jugador_id).first()
                if existing:
                    existing.activo = False
                    db.commit()
                    logger.info(f"Jugador eliminado (soft delete): {jugador_id}")
                    return existing
                return None
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Error en soft delete del jugador {jugador_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al eliminar jugador"
                )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar jugador {jugador_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar jugador"
        )
