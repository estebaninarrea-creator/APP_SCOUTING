from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ArbitroBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=120, description="Nombre del árbitro")
    apellido: str = Field(..., min_length=1, max_length=120, description="Apellido del árbitro")
    documento: str | None = Field(None, max_length=30, description="Documento de identidad")
    liga_id: UUID | None = Field(None, description="ID de la liga (opcional)")
    activo: bool = Field(True, description="Árbitro activo")


class ArbitroCreate(ArbitroBase):
    pass


class ArbitroUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=120, description="Nombre del árbitro")
    apellido: str | None = Field(None, min_length=1, max_length=120, description="Apellido del árbitro")
    documento: str | None = Field(None, max_length=30, description="Documento de identidad")
    liga_id: UUID | None = Field(None, description="ID de la liga")
    activo: bool | None = Field(None, description="Árbitro activo")


class ArbitroResponse(ArbitroBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
