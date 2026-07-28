from datetime import date, datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Clubes(Base):
    __tablename__ = "clubes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    comet_id: Mapped[int | None] = mapped_column(
        BigInteger
    )

    nombre_corto: Mapped[str | None] = mapped_column(
        String(50)
    )

    sigla: Mapped[str | None] = mapped_column(
        String(10)
    )

    ciudad_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ciudades.id")
    )

    direccion: Mapped[str | None] = mapped_column(
        String(200)
    )

    telefono: Mapped[str | None] = mapped_column(
        String(50)
    )

    email: Mapped[str | None] = mapped_column(
        String(150)
    )

    sitio_web: Mapped[str | None] = mapped_column(
        Text
    )

    escudo_url: Mapped[str | None] = mapped_column(
        Text
    )

    fundacion: Mapped[date | None] = mapped_column(
        Date
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    ciudad = relationship(
        "Ciudades",
        back_populates="clubes"
    )

    equipos = relationship(
        "Equipos",
        back_populates="club",
        cascade="all,delete-orphan",
    )

    estadios = relationship(
        "Estadios",
        back_populates="club",
        cascade="all,delete-orphan",
    )
