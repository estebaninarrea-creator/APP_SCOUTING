from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EquipoBase(BaseModel):
    club_id: UUID = Field(..., description="ID del club")
    temporada_id: UUID = Field(..., description="ID de la temporada")
    categoria_id: UUID = Field(..., description="ID de la categoría")
    nombre: str | None = Field(None, max_length=120, description="Nombre del equipo")
    director_tecnico: str | None = Field(None, max_length=120, description="Director técnico")
    ayudante_tecnico: str | None = Field(None, max_length=120, description="Ayudante técnico")
    preparador_fisico: str | None = Field(None, max_length=120, description="Preparador físico")


class EquipoCreate(EquipoBase):
    pass


class EquipoUpdate(EquipoBase):
    pass


class EquipoResponse(EquipoBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
