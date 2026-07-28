from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClubBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nombre del club"
    )
    activo: bool = Field(
        True,
        description="Si el club está activo"
    )
    comet_id: int | None = Field(
        None,
        ge=1,
        description="ID COMET externo"
    )
    nombre_corto: str | None = Field(
        None,
        max_length=50,
        description="Nombre corto (sigla)"
    )
    sigla: str | None = Field(
        None,
        min_length=1,
        max_length=5,
        description="Sigla del club"
    )
    ciudad_id: UUID | None = Field(
        None,
        description="ID de la ciudad"
    )
    direccion: str | None = Field(
        None,
        max_length=255,
        description="Dirección del club"
    )
    telefono: str | None = Field(
        None,
        min_length=5,
        max_length=20,
        description="Teléfono de contacto"
    )
    email: str | None = Field(
        None,
        max_length=255,
        description="Email del club"
    )
    sitio_web: str | None = Field(
        None,
        max_length=255,
        description="Sitio web del club"
    )
    escudo_url: str | None = Field(
        None,
        max_length=500,
        description="URL del escudo"
    )
    fundacion: date | None = Field(
        None,
        description="Fecha de fundación"
    )
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v and "@" not in v:
            raise ValueError("Email inválido")
        return v


class ClubCreate(ClubBase):
    pass


class ClubUpdate(ClubBase):
    pass


class ClubResponse(ClubBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
