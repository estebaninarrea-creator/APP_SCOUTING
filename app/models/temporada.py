from datetime import date, datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Temporadas(Base):
    __tablename__ = "temporadas"

    __table_args__ = (
        UniqueConstraint(
            "liga_id",
            "nombre",
            name="uk_temporada",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    liga_id: Mapped[UUID] = mapped_column(
        ForeignKey("ligas.id"),
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    fecha_fin: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    activa: Mapped[bool | None] = mapped_column(
        Boolean,
        server_default=text("false"),
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    liga = relationship(
        "Ligas",
        back_populates="temporadas",
    )

    equipos = relationship(
        "Equipos",
        back_populates="temporada",
        cascade="all,delete-orphan",
    )

    torneos = relationship(
        "Torneos",
        back_populates="temporada",
        cascade="all,delete-orphan",
    )
