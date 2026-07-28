from datetime import date, datetime, time
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator


class PartidoBase(BaseModel):
    torneo_id: UUID | None = Field(
        None,
        description="ID del torneo"
    )
    equipo_local_id: UUID | None = Field(
        None,
        description="ID del equipo local",
        validation_alias=AliasChoices("equipo_local_id", "local_equipo_id"),
    )
    equipo_visitante_id: UUID | None = Field(
        None,
        description="ID del equipo visitante",
        validation_alias=AliasChoices("equipo_visitante_id", "visitante_equipo_id"),
    )
    estado_id: UUID | None = Field(
        None,
        description="ID del estado del partido"
    )
    comet_id: int | None = Field(
        None,
        ge=1,
        description="ID COMET externo"
    )
    fecha_partido: date | None = Field(
        None,
        description="Fecha del partido"
    )
    hora: time | None = Field(
        None,
        description="Hora de inicio"
    )
    cancha_id: UUID | None = Field(
        None,
        description="ID de la cancha"
    )
    arbitro_id: UUID | None = Field(
        None,
        description="ID del árbitro"
    )
    goles_local: int | None = Field(
        None,
        ge=0,
        le=50,
        description="Goles del equipo local (0-50)"
    )
    goles_visitante: int | None = Field(
        None,
        ge=0,
        le=50,
        description="Goles del equipo visitante (0-50)"
    )
    observaciones: str | None = Field(
        None,
        max_length=1000,
        description="Observaciones del partido"
    )
    
    @field_validator("goles_local", "goles_visitante")
    @classmethod
    def validate_goles(cls, v):
        if v is not None and v < 0:
            raise ValueError("Los goles no pueden ser negativos")
        return v


class PartidoCreate(PartidoBase):
    estado_manual: bool = Field(
        False,
        description="Cuando es true y se envía estado_id, fuerza el estado manual sin automatización",
    )


class PartidoUpdate(PartidoBase):
    estado_manual: bool | None = Field(
        None,
        description="Cuando es true y se envía estado_id, fuerza el estado manual sin automatización",
    )


class PartidoResponse(PartidoBase):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
