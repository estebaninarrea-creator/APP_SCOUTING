from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LigaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120, description="Nombre de la liga")
    comet_id: int | None = Field(None, ge=1, description="ID COMET externo")
    pais_id: UUID | None = Field(None, description="ID del país")
    provincia_id: UUID | None = Field(None, description="ID de la provincia")
    logo_url: str | None = Field(None, max_length=500, description="URL del logo")
    sitio_web: str | None = Field(None, max_length=255, description="Sitio web")
    email: str | None = Field(None, max_length=100, description="Email de contacto")
    telefono: str | None = Field(None, max_length=20, description="Teléfono")
    activo: bool = Field(True, description="Liga activa")


class LigaCreate(LigaBase):
    pass


class LigaUpdate(LigaBase):
    pass


class LigaResponse(LigaBase):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
