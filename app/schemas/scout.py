from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ScoutBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del scout")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del scout")
    usuario_id: UUID = Field(..., description="ID del usuario asociado")
    telefono: str | None = Field(None, max_length=20, description="Teléfono")
    email: str | None = Field(None, max_length=100, description="Email")
    activo: bool = Field(True, description="Scout activo")


class ScoutCreate(ScoutBase):
    pass


class ScoutUpdate(ScoutBase):
    pass


class ScoutResponse(ScoutBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
