from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=60, description="Nombre de la categoría")
    sexo: str = Field(default="M", min_length=1, max_length=1, description="Sexo: M (Masculino), F (Femenino), X (Mixto)")
    edad_min: int | None = Field(None, ge=0, le=100, description="Edad mínima")
    edad_max: int | None = Field(None, ge=0, le=100, description="Edad máxima")


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=60)
    sexo: str | None = Field(None, min_length=1, max_length=1)
    edad_min: int | None = Field(None, ge=0, le=100)
    edad_max: int | None = Field(None, ge=0, le=100)


class CategoriaResponse(CategoriaBase):
    id: UUID
    created_at: datetime

    class ConfigDict:
        from_attributes = True
