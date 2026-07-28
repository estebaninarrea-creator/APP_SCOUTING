from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PartidoJugadorBase(BaseModel):
    jugador_id: UUID = Field(..., description="ID del jugador")
    numero_camiseta: int | None = Field(None, ge=0, le=99, description="Número de camiseta")
    posicion: str | None = Field(None, max_length=50, description="Posición del jugador")
    minutos_jugados: int | None = Field(None, ge=0, le=180, description="Minutos jugados")


class PartidoJugadorCreate(PartidoJugadorBase):
    pass


class PartidoJugadorUpdate(BaseModel):
    jugador_id: UUID | None = None
    numero_camiseta: int | None = Field(None, ge=0, le=99)
    posicion: str | None = Field(None, max_length=50)
    minutos_jugados: int | None = Field(None, ge=0, le=180)


class PartidoJugadorResponse(PartidoJugadorBase):
    id: UUID
    partido_id: UUID
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
