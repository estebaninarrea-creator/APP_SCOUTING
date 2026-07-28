from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CanchaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str | None = Field(None, max_length=1000)


class CanchaCreate(CanchaBase):
    pass


class CanchaUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    descripcion: str | None = Field(None, max_length=1000)


class CanchaResponse(CanchaBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
