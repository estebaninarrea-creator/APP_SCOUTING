from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PlantelBase(BaseModel):
    equipo_id: UUID = Field(..., description="ID del equipo")
    jugador_id: UUID = Field(..., description="ID del jugador")
    fecha_desde: date = Field(..., description="Fecha desde que está en el plantel")
    dorsal: int | None = Field(None, ge=1, le=99, description="Número de dorsal")
    fecha_hasta: date | None = Field(None, description="Fecha hasta que está en el plantel")
    activo: bool = Field(default=True, description="¿Está activo en el plantel?")


class PlantelCreate(PlantelBase):
    pass


class PlantelUpdate(BaseModel):
    equipo_id: UUID | None = Field(None, description="ID del equipo")
    jugador_id: UUID | None = Field(None, description="ID del jugador")
    fecha_desde: date | None = Field(None, description="Fecha desde")
    dorsal: int | None = Field(None, ge=1, le=99, description="Número de dorsal")
    fecha_hasta: date | None = Field(None, description="Fecha hasta")
    activo: bool | None = Field(None, description="¿Está activo?")


class PlantelResponse(PlantelBase):
    id: UUID
    created_at: datetime

    class ConfigDict:
        from_attributes = True
