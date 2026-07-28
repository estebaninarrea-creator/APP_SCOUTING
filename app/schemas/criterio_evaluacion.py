from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CriterioEvaluacionBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=120)
    descripcion: str | None = None
    activo: bool = True


class CriterioEvaluacionCreate(CriterioEvaluacionBase):
    pass


class CriterioEvaluacionUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=120)
    descripcion: str | None = None
    activo: bool | None = None


class CriterioEvaluacionResponse(CriterioEvaluacionBase):
    id: UUID
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
