import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.rbac import AVAILABLE_PERMISSIONS, get_role_permission_matrix, set_permissions_for_role
from app.models.rol import Roles
from app.schemas.rol import RolCreate, RolUpdate

logger = logging.getLogger(__name__)


def get_roles(db: Session):
    logger.info("Obteniendo todos los roles")
    try:
        result = db.query(Roles).order_by(Roles.nombre).all()
        logger.info(f"Se obtuvieron {len(result)} roles")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener roles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener roles")


def get_rol(db: Session, rol_id):
    logger.info(f"Obteniendo rol {rol_id}")
    try:
        result = db.query(Roles).filter(Roles.id == rol_id).first()
        if not result:
            logger.warning(f"Rol no encontrado: {rol_id}")
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener rol {rol_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener rol")


def create_rol(db: Session, rol: RolCreate):
    logger.info(f"Creando nuevo rol")
    try:
        nuevo = Roles(**rol.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Rol creado: {nuevo.id}")
        return nuevo
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: violación de restricción")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear rol: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear rol")


def update_rol(db: Session, rol_id, rol: RolUpdate):
    logger.info(f"Actualizando rol {rol_id}")
    try:
        existing = get_rol(db, rol_id)
        for key, value in rol.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Rol actualizado: {rol_id}")
        return existing
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: violación de restricción")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar rol {rol_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar rol")


def delete_rol(db: Session, rol_id):
    logger.info(f"Eliminando rol {rol_id}")
    try:
        rol = get_rol(db, rol_id)
        db.delete(rol)
        db.commit()
        logger.info(f"Rol eliminado: {rol_id}")
        return rol
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="No se puede eliminar el rol")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar rol {rol_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar rol")


def get_permissions_matrix():
    return {
        "available_permissions": sorted(AVAILABLE_PERMISSIONS),
        "matrix": get_role_permission_matrix(),
    }


def update_role_permissions(db: Session, rol_id: UUID, permissions: list[str]):
    rol = get_rol(db, rol_id)
    updated_permissions = set_permissions_for_role(rol.nombre, permissions)
    return {
        "role_id": rol.id,
        "role_name": rol.nombre,
        "permissions": updated_permissions,
    }
