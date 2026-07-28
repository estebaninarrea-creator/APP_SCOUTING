from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Torneos(Base):
    __tablename__ = "torneos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    temporada_id: Mapped[UUID] = mapped_column(
        ForeignKey("temporadas.id"),
        nullable=False
    )

    categoria_id: Mapped[UUID] = mapped_column(
        ForeignKey("categorias.id"),
        nullable=False
    )

    tipo_torneo_id: Mapped[UUID] = mapped_column(
        ForeignKey("tipos_torneo.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    comet_id: Mapped[int | None]

    fecha_inicio: Mapped[date | None] = mapped_column(Date)

    fecha_fin: Mapped[date | None] = mapped_column(Date)

    activo: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)

    temporada = relationship(
        "Temporadas",
        back_populates="torneos"
    )

    categoria = relationship(
        "Categorias",
        back_populates="torneos"
    )

    tipo_torneo = relationship(
        "TiposTorneo",
        back_populates="torneos"
    )

    torneos_clubes = relationship(
        "TorneosClubes",
        back_populates="torneo",
        cascade="all,delete-orphan",
    )

    partidos = relationship(
        "Partidos",
        back_populates="torneo",
        foreign_keys="Partidos.torneo_id",
        cascade="all,delete-orphan",
    )
