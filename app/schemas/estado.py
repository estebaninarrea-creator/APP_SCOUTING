from pydantic import BaseModel, Field
from uuid import UUID


class EstadoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del estado")
    descripcion: str | None = Field(None, max_length=255, description="Descripción del estado")


class EstadoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=50, description="Nombre del estado")
    descripcion: str | None = Field(None, max_length=255, description="Descripción del estado")


class EstadoResponse(BaseModel):
    id: UUID
    nombre: str
    descripcion: str | None = None

    model_config = {"from_attributes": True}
