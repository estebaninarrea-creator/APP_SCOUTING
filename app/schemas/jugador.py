from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator, Field


class PosicionJugadorPayload(BaseModel):
    id: UUID
    principal: bool = False


class JugadorBase(BaseModel):
    apellido: str | None = Field(
        None,
        min_length=2,
        max_length=120,
        description="Apellido del jugador"
    )
    nombre: str | None = Field(
        None,
        min_length=2,
        max_length=120,
        description="Nombre del jugador"
    )
    comet_id: int | None = Field(
        None,
        ge=1,
        description="ID COMET externo"
    )
    documento: str | None = Field(
        None,
        min_length=5,
        max_length=30,
        description="Documento de identidad"
    )
    fecha_nacimiento: date | None = Field(
        None,
        description="Fecha de nacimiento"
    )
    pais_id: UUID | None = Field(
        None,
        description="ID del país"
    )
    ciudad_id: UUID | None = Field(
        None,
        description="ID de la ciudad"
    )
    altura: Decimal | None = Field(
        None,
        ge=Decimal("1.40"),
        le=Decimal("2.30"),
        description="Altura en metros (1.40 a 2.30)"
    )
    peso: Decimal | None = Field(
        None,
        ge=Decimal("40"),
        le=Decimal("150"),
        description="Peso en kg (40 a 150)"
    )
    pierna_habil: str | None = Field(
        None,
        description="Pierna hábil: D (derecha), I (izquierda), A (ambas)"
    )
    foto_url: str | None = Field(
        None,
        max_length=500,
        description="URL de la foto del jugador"
    )
    activo: bool | None = Field(
        None,
        description="Si el jugador está activo"
    )
    posiciones: list[PosicionJugadorPayload] | None = Field(
        None,
        description="Posiciones del jugador"
    )

    @field_validator("pierna_habil")
    @classmethod
    def validate_pierna_habil(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip().lower()
        mapping = {
            "d": "D",
            "derecha": "D",
            "right": "D",
            "i": "I",
            "izquierda": "I",
            "left": "I",
            "a": "A",
            "ambas": "A",
            "both": "A",
        }
        if normalized in mapping:
            return mapping[normalized]
        if normalized in {"d", "i", "a"}:
            return normalized.upper()
        raise ValueError("Pierna hábil debe ser: D (derecha), I (izquierda) o A (ambas)")


class JugadorCreate(JugadorBase):
    apellido: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Apellido del jugador (requerido)"
    )
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nombre del jugador (requerido)"
    )

    comet_id: int | None = None

    documento: str | None = None

    fecha_nacimiento: date | None = None

    pais_id: UUID | None = None

    ciudad_id: UUID | None = None

    altura: Decimal | None = None

    peso: Decimal | None = None

    pierna_habil: str | None = None

    foto_url: str | None = None
    posiciones: list[PosicionJugadorPayload] | None = None


class JugadorUpdate(JugadorBase):
    pass


class JugadorResponse(BaseModel):
    id: UUID
    apellido: str | None = None
    nombre: str | None = None
    comet_id: int | None = None
    documento: str | None = None
    fecha_nacimiento: date | None = None
    pais_id: UUID | None = None
    ciudad_id: UUID | None = None
    altura: Decimal | None = None
    peso: Decimal | None = None
    pierna_habil: str | None = None
    foto_url: str | None = None
    activo: bool | None = None
    posiciones: list[PosicionJugadorPayload] = Field(default_factory=list)

    # Response model must tolerate legacy rows already persisted in DB.
    model_config = ConfigDict(from_attributes=True)
