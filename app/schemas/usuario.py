from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UsuarioBase(BaseModel):
    rol_id: UUID = Field(
        ...,
        description="ID del rol"
    )
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nombre del usuario"
    )
    apellido: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Apellido del usuario"
    )
    email: EmailStr = Field(
        ...,
        description="Email válido del usuario"
    )
    activo: bool = Field(
        True,
        description="Si el usuario está activo"
    )


class UsuarioCreate(UsuarioBase):
    password_hash: str = Field(
        ...,
        min_length=8,
        description="Hash de la contraseña (bcrypt)"
    )


class UsuarioUpdate(BaseModel):
    rol_id: UUID | None = Field(
        None,
        description="ID del rol"
    )
    nombre: str | None = Field(
        None,
        min_length=2,
        max_length=120,
        description="Nombre del usuario"
    )
    apellido: str | None = Field(
        None,
        min_length=2,
        max_length=120,
        description="Apellido del usuario"
    )
    email: EmailStr | None = Field(
        None,
        description="Email válido del usuario"
    )
    activo: bool | None = Field(
        None,
        description="Si el usuario está activo"
    )
    password_hash: str | None = Field(
        None,
        min_length=8,
        description="Nueva contraseña en texto plano para volver a hashearla"
    )


class UsuarioResponse(UsuarioBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
