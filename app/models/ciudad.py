from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Ciudades(Base):
    __tablename__ = "ciudades"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    provincia_id: Mapped[UUID] = mapped_column(
        ForeignKey("provincias.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    codigo_postal: Mapped[str | None]

    latitud: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7)
    )

    longitud: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    provincia = relationship(
        "Provincias",
        back_populates="ciudades"
    )

    clubes = relationship(
        "Clubes",
        back_populates="ciudad",
        cascade="all,delete-orphan",
    )

    jugadores = relationship(
        "Jugadores",
        back_populates="ciudad",
        cascade="all,delete-orphan",
    )

    estadios = relationship(
        "Estadios",
        back_populates="ciudad",
        cascade="all,delete-orphan",
    )
