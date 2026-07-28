from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RolBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del rol")
    descripcion: str | None = Field(None, max_length=255, description="Descripción del rol")


class RolCreate(RolBase):
    pass


class RolUpdate(RolBase):
    pass


class RolResponse(RolBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class RolePermissionsUpdate(BaseModel):
    permissions: list[str] = Field(default_factory=list, description="Permisos asignados al rol")


class RolePermissionsResponse(BaseModel):
    role_id: UUID
    role_name: str
    permissions: list[str] = Field(default_factory=list)


class RolePermissionsMatrixResponse(BaseModel):
    available_permissions: list[str] = Field(default_factory=list)
    matrix: dict[str, list[str]] = Field(default_factory=dict)
