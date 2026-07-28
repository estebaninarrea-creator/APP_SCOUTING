from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class InformeScoutingBase(BaseModel):
    jugador_id: UUID = Field(..., description="ID del jugador")
    scout_id: UUID = Field(..., description="ID del scout")
    observaciones: str | None = Field(None, max_length=2000, description="Observaciones del scouting")


class InformeScoutingCreate(InformeScoutingBase):
    pass


class InformeScoutingUpdate(BaseModel):
    jugador_id: UUID | None = None
    scout_id: UUID | None = None
    observaciones: str | None = None


class InformeScoutingResponse(InformeScoutingBase):
    id: UUID
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class EvaluacionJugadorBase(BaseModel):
    jugador_id: UUID
    partido_id: UUID
    scout_id: UUID
    criterio_id: UUID
    valor: int
    comentario: str | None = None


class EvaluacionJugadorCreate(EvaluacionJugadorBase):
    pass


class EvaluacionJugadorUpdate(BaseModel):
    jugador_id: UUID | None = None
    partido_id: UUID | None = None
    scout_id: UUID | None = None
    criterio_id: UUID | None = None
    valor: int | None = None
    comentario: str | None = None


class EvaluacionJugadorResponse(EvaluacionJugadorBase):
    id: UUID
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class VideoBase(BaseModel):
    jugador_id: UUID
    partido_id: UUID | None = None
    url: str
    descripcion: str | None = None


class VideoCreate(VideoBase):
    pass


class VideoUpdate(BaseModel):
    jugador_id: UUID | None = None
    partido_id: UUID | None = None
    url: str | None = None
    descripcion: str | None = None


class VideoResponse(VideoBase):
    id: UUID
    fecha_carga: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ArchivoAdjuntoBase(BaseModel):
    jugador_id: UUID | None = None
    partido_id: UUID | None = None
    nombre_archivo: str
    ruta_archivo: str
    tipo_archivo: str | None = None


class ArchivoAdjuntoCreate(ArchivoAdjuntoBase):
    pass


class ArchivoAdjuntoUpdate(BaseModel):
    jugador_id: UUID | None = None
    partido_id: UUID | None = None
    nombre_archivo: str | None = None
    ruta_archivo: str | None = None
    tipo_archivo: str | None = None


class ArchivoAdjuntoResponse(ArchivoAdjuntoBase):
    id: UUID
    fecha_carga: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

