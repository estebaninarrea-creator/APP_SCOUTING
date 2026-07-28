from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TipoTorneoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del tipo de torneo")


class TipoTorneoCreate(TipoTorneoBase):
    pass


class TipoTorneoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=50)


class TipoTorneoResponse(TipoTorneoBase):
    id: UUID
    created_at: datetime

    class ConfigDict:
        from_attributes = True
