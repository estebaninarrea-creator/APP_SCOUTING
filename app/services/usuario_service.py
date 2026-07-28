from uuid import UUID
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.usuario import Usuarios
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

logger = logging.getLogger(__name__)


def get_usuarios(db: Session):
    """Obtiene todos los usuarios"""
    try:
        return db.query(Usuarios).order_by(Usuarios.apellido, Usuarios.nombre).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuarios: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener usuarios"
        )


def get_usuario(db: Session, usuario_id: UUID):
    """Obtiene un usuario por ID"""
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario {usuario_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener usuario"
        )


def create_usuario(db: Session, usuario: UsuarioCreate):
    """Crea un nuevo usuario"""
    try:
        usuario_data = usuario.model_dump(exclude_unset=True)
        usuario_data["password_hash"] = hash_password(usuario_data["password_hash"])
        nuevo = Usuarios(**usuario_data)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Usuario creado: {nuevo.id} ({nuevo.email})")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al crear usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: email duplicado o violación de restricción"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear usuario"
        )


def update_usuario(db: Session, usuario_id: UUID, usuario: UsuarioUpdate):
    """Actualiza un usuario existente"""
    try:
        existing = get_usuario(db, usuario_id)
        update_data = usuario.model_dump(exclude_unset=True)
        if update_data.get("password_hash"):
            update_data["password_hash"] = hash_password(update_data["password_hash"])

        for key, value in update_data.items():
            if value is not None:
                setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Usuario actualizado: {usuario_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al actualizar usuario {usuario_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: email duplicado o violación de restricción"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario {usuario_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar usuario"
        )


def delete_usuario(db: Session, usuario_id: UUID):
    """Elimina un usuario"""
    try:
        existing = get_usuario(db, usuario_id)
        db.delete(existing)
        db.commit()
        logger.info(f"Usuario eliminado: {usuario_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Error de integridad al eliminar usuario {usuario_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar: existen registros relacionados"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar usuario {usuario_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar usuario"
        )
