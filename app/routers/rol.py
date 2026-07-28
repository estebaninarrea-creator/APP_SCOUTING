from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.rol import (
    RolCreate,
    RolResponse,
    RolUpdate,
    RolePermissionsMatrixResponse,
    RolePermissionsResponse,
    RolePermissionsUpdate,
)
from app.services.rol_service import (
    create_rol,
    delete_rol,
    get_permissions_matrix,
    get_roles,
    get_rol,
    update_role_permissions,
    update_rol,
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.get("/", response_model=list[RolResponse])
def listar_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.get("/permissions", response_model=RolePermissionsMatrixResponse)
def obtener_matriz_permisos():
    return get_permissions_matrix()


@router.get("/{rol_id}", response_model=RolResponse)
def obtener_rol(
    rol_id: UUID,
    db: Session = Depends(get_db),
):
    rol = get_rol(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.put("/{rol_id}/permissions", response_model=RolePermissionsResponse)
def actualizar_permisos_rol(
    rol_id: UUID,
    payload: RolePermissionsUpdate,
    db: Session = Depends(get_db),
):
    updated = update_role_permissions(db, rol_id, payload.permissions)
    if not updated:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return updated


@router.post("/", response_model=RolResponse)
def crear_rol(
    rol: RolCreate,
    db: Session = Depends(get_db),
):
    return create_rol(db, rol)


@router.put("/{rol_id}", response_model=RolResponse)
def actualizar_rol(
    rol_id: UUID,
    rol: RolUpdate,
    db: Session = Depends(get_db),
):
    updated = update_rol(db, rol_id, rol)
    if not updated:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return updated


@router.delete("/{rol_id}")
def eliminar_rol(
    rol_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = delete_rol(db, rol_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"mensaje": "Rol eliminado"}
