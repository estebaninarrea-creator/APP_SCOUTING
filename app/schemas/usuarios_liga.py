from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UsuarioLigaCreate(BaseModel):
    usuario_id: UUID
    liga_id: UUID


class UsuarioLigaResponse(BaseModel):
    usuario_id: UUID
    liga_id: UUID

    model_config = ConfigDict(from_attributes=True)
