from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CanchaBase(BaseModel):
    estadio_id: UUID
    nombre: str = Field(..., min_length=1, max_length=100)
    tipo_superficie: str | None = Field(None, max_length=30)
    iluminacion: bool = False
    habilitada: bool = True


class CanchaCreate(CanchaBase):
    pass


class CanchaUpdate(BaseModel):
    estadio_id: UUID | None = None
    nombre: str | None = Field(None, min_length=1, max_length=100)
    tipo_superficie: str | None = Field(None, max_length=30)
    iluminacion: bool | None = None
    habilitada: bool | None = None


class CanchaResponse(CanchaBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
