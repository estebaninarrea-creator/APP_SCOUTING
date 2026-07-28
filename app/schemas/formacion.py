from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FormacionBase(BaseModel):
    partido_id: UUID = Field(..., description="ID del partido")
    equipo_id: UUID = Field(..., description="ID del equipo")
    esquema: str | None = Field(None, description="Esquema táctico (ej: 4-3-3)")


class FormacionCreate(FormacionBase):
    pass


class FormacionUpdate(BaseModel):
    partido_id: UUID | None = Field(None, description="ID del partido")
    equipo_id: UUID | None = Field(None, description="ID del equipo")
    esquema: str | None = Field(None, description="Esquema táctico")


class FormacionResponse(FormacionBase):
    id: UUID
    created_at: datetime

    class ConfigDict:
        from_attributes = True
