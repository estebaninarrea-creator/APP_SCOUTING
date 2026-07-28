from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TorneoBase(BaseModel):
    temporada_id: UUID = Field(..., description="ID de la temporada")
    categoria_id: UUID = Field(..., description="ID de la categoría")
    tipo_torneo_id: UUID = Field(..., description="ID del tipo de torneo")
    nombre: str = Field(..., min_length=2, max_length=120, description="Nombre del torneo")
    comet_id: int | None = Field(None, ge=1, description="ID COMET externo")
    fecha_inicio: date | None = Field(None, description="Fecha de inicio")
    fecha_fin: date | None = Field(None, description="Fecha de fin")
    activo: bool = Field(True, description="Torneo activo")


class TorneoCreate(TorneoBase):
    pass


class TorneoUpdate(TorneoBase):
    pass


class TorneoResponse(TorneoBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
