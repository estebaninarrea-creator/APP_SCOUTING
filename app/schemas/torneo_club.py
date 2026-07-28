from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TorneoClubCreate(BaseModel):
    torneo_id: UUID
    equipo_id: UUID
    zona: str | None = Field(None, max_length=120)
    grupo: str | None = Field(None, max_length=120)


class TorneoClubUpdate(BaseModel):
    zona: str | None = Field(None, max_length=120)
    grupo: str | None = Field(None, max_length=120)


class TorneoClubResponse(BaseModel):
    torneo_id: UUID
    equipo_id: UUID
    zona: str | None = None
    grupo: str | None = None

    model_config = ConfigDict(from_attributes=True)
