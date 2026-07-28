from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Ligas(Base):
    __tablename__ = "ligas"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    comet_id: Mapped[int | None] = mapped_column(
        BigInteger
    )

    pais_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("paises.id")
    )

    provincia_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("provincias.id")
    )

    logo_url: Mapped[str | None] = mapped_column(
        Text
    )

    sitio_web: Mapped[str | None] = mapped_column(
        Text
    )

    email: Mapped[str | None] = mapped_column(
        String(150)
    )

    telefono: Mapped[str | None] = mapped_column(
        String(50)
    )

    activo: Mapped[bool | None] = mapped_column(
        Boolean,
        server_default=text("true")
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    pais = relationship(
        "Paises",
        back_populates="ligas"
    )

    provincia = relationship(
        "Provincias",
        back_populates="ligas"
    )

    usuarios = relationship(
        "Usuarios",
        secondary="usuarios_ligas",
        back_populates="ligas"
    )

    arbitros = relationship(
        "Arbitros",
        back_populates="liga",
        cascade="all,delete-orphan",
    )

    temporadas = relationship(
        "Temporadas",
        back_populates="liga",
        cascade="all,delete-orphan",
    )
