from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EstadioBase(BaseModel):
    club_id: UUID
    nombre: str = Field(..., min_length=1, max_length=150)
    direccion: str | None = Field(None, max_length=200)
    ciudad_id: UUID | None = None
    capacidad: int | None = Field(None, ge=0)
    latitud: Decimal | None = None
    longitud: Decimal | None = None


class EstadioCreate(EstadioBase):
    pass


class EstadioUpdate(BaseModel):
    club_id: UUID | None = None
    nombre: str | None = Field(None, min_length=1, max_length=150)
    direccion: str | None = Field(None, max_length=200)
    ciudad_id: UUID | None = None
    capacidad: int | None = Field(None, ge=0)
    latitud: Decimal | None = None
    longitud: Decimal | None = None


class EstadioResponse(EstadioBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
