from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PaisBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nombre del país"
    )
    codigo_iso2: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Código ISO-2 (ej: AR, BR)"
    )
    codigo_iso3: str | None = Field(
        None,
        min_length=3,
        max_length=3,
        description="Código ISO-3 (ej: ARG, BRA)"
    )
    codigo_fifa: str | None = Field(
        None,
        min_length=3,
        max_length=3,
        description="Código FIFA"
    )
    
    @field_validator("codigo_iso2")
    @classmethod
    def validate_iso2(cls, v):
        if v and not v.isupper() or len(v) != 2:
            raise ValueError("Código ISO-2 debe ser 2 caracteres en mayúscula")
        return v


class PaisCreate(PaisBase):
    pass


class PaisUpdate(BaseModel):
    nombre: str | None = Field(
        None,
        min_length=2,
        max_length=120,
        description="Nombre del país"
    )
    codigo_iso2: str | None = Field(
        None,
        min_length=2,
        max_length=2,
        description="Código ISO-2"
    )
    codigo_iso3: str | None = Field(
        None,
        min_length=3,
        max_length=3,
        description="Código ISO-3"
    )
    codigo_fifa: str | None = Field(
        None,
        min_length=3,
        max_length=3,
        description="Código FIFA"
    )


class PaisResponse(PaisBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProvinciaBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nombre de la provincia"
    )
    pais_id: UUID | None = Field(
        None,
        description="ID del país"
    )


class ProvinciaCreate(ProvinciaBase):
    pass


class ProvinciaUpdate(BaseModel):
    nombre: str | None = Field(
        None,
        min_length=2,
        max_length=120,
        description="Nombre de la provincia"
    )
    pais_id: UUID | None = Field(
        None,
        description="ID del país"
    )


class ProvinciaResponse(ProvinciaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class CiudadBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nombre de la ciudad"
    )
    provincia_id: UUID | None = Field(
        None,
        description="ID de la provincia"
    )
    codigo_postal: str | None = Field(
        None,
        max_length=20,
        description="Código postal"
    )


class CiudadCreate(CiudadBase):
    pass


class CiudadUpdate(BaseModel):
    nombre: str | None = Field(
        None,
        min_length=2,
        max_length=120,
        description="Nombre de la ciudad"
    )
    provincia_id: UUID | None = Field(
        None,
        description="ID de la provincia"
    )
    codigo_postal: str | None = Field(
        None,
        max_length=20,
        description="Código postal"
    )


class CiudadResponse(CiudadBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class PosicionBase(BaseModel):
    codigo: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Código de la posición (ej: POR, DEF, MED, DEL)"
    )
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre de la posición"
    )
    orden: int | None = Field(
        None,
        ge=0,
        le=100,
        description="Orden de visualización"
    )


class PosicionCreate(PosicionBase):
    pass


class PosicionUpdate(BaseModel):
    codigo: str | None = Field(
        None,
        min_length=1,
        max_length=10,
        description="Código de la posición"
    )
    nombre: str | None = Field(
        None,
        min_length=2,
        max_length=50,
        description="Nombre de la posición"
    )
    orden: int | None = Field(
        None,
        ge=1,
        le=100,
        description="Orden de visualización"
    )


class PosicionResponse(PosicionBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProvinciaResponseLite(BaseModel):
    id: UUID
    nombre: str
    pais_id: UUID

    model_config = ConfigDict(from_attributes=True)


class CiudadResponseLite(BaseModel):
    id: UUID
    nombre: str
    provincia_id: UUID

    model_config = ConfigDict(from_attributes=True)


class TemporadaMaestraResponse(BaseModel):
    id: UUID
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class CategoriaMaestraResponse(BaseModel):
    id: UUID
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class TipoTorneoMaestraResponse(BaseModel):
    id: UUID
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class DatosMaestrosResponse(BaseModel):
    provincias: list[ProvinciaResponseLite]
    ciudades: list[CiudadResponseLite]
    posiciones: list[PosicionResponse]
    temporadas: list[TemporadaMaestraResponse]
    categorias: list[CategoriaMaestraResponse]
    tipos_torneo: list[TipoTorneoMaestraResponse]

    model_config = ConfigDict(from_attributes=True)
