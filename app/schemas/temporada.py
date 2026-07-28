from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TemporadaBase(BaseModel):
    liga_id: UUID = Field(..., description="ID de la liga")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la temporada")
    fecha_inicio: date = Field(..., description="Fecha de inicio")
    fecha_fin: date = Field(..., description="Fecha de fin")
    activa: bool = Field(True, description="Temporada activa")


class TemporadaCreate(TemporadaBase):
    pass


class TemporadaUpdate(BaseModel):
    liga_id: UUID | None = None
    nombre: str | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    activa: bool | None = None


class TemporadaResponse(TemporadaBase):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
