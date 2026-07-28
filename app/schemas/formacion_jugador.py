from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FormacionJugadorBase(BaseModel):
    formacion_id: UUID
    jugador_id: UUID
    numero_camiseta: int | None = Field(None, ge=0)
    posicion_id: UUID | None = None


class FormacionJugadorCreate(FormacionJugadorBase):
    pass


class FormacionJugadorUpdate(BaseModel):
    numero_camiseta: int | None = Field(None, ge=0)
    posicion_id: UUID | None = None


class FormacionJugadorResponse(FormacionJugadorBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
