from uuid import UUID
import logging

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

from app.models.club import Clubes
from app.models.equipo import Equipos
from app.models.estadio import Estadios
from app.schemas.club import ClubCreate, ClubUpdate

logger = logging.getLogger(__name__)


def get_clubes(db: Session):
    """Obtiene todos los clubes"""
    try:
        return db.query(Clubes).order_by(Clubes.nombre).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener clubes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener clubes"
        )


def get_club(db: Session, club_id: UUID):
    """Obtiene un club por ID"""
    try:
        club = db.query(Clubes).filter(Clubes.id == club_id).first()
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Club no encontrado"
            )
        return club
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener club {club_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener club"
        )


def create_club(db: Session, club: ClubCreate):
    """Crea un nuevo club"""
    try:
        nuevo = Clubes(**club.model_dump(exclude_unset=True))
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Club creado: {nuevo.id} ({nuevo.nombre})")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al crear club: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción (posiblemente nombre duplicado)"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear club: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear club"
        )


def update_club(db: Session, club_id: UUID, club: ClubUpdate):
    """Actualiza un club existente"""
    try:
        existing = get_club(db, club_id)
        for key, value in club.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Club actualizado: {club_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al actualizar club {club_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: violación de restricción"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar club {club_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar club"
        )


def delete_club(db: Session, club_id: UUID):
    """Elimina un club (con validación de dependencias)"""
    try:
        existing = get_club(db, club_id)

        has_team_dependency = db.query(Equipos).filter(Equipos.club_id == club_id).first() is not None
        has_stadium_dependency = db.query(Estadios).filter(Estadios.club_id == club_id).first() is not None

        if has_team_dependency or has_stadium_dependency:
            logger.warning(f"Intento de eliminar club {club_id} con dependencias")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el club porque tiene equipos o estadios relacionados"
            )

        db.delete(existing)
        db.commit()
        logger.info(f"Club eliminado: {club_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al eliminar club {club_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar: existen registros relacionados"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar club {club_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar club"
        )
