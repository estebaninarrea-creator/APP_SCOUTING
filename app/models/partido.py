from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, Time, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Partidos(Base):
    __tablename__ = "partidos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    torneo_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("torneos.id"),
        nullable=True,
    )

    fecha_partido: Mapped[date | None] = mapped_column(
        "fecha",
        Date,
        nullable=True,
    )

    equipo_local_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("equipos.id"),
        nullable=True,
    )

    equipo_visitante_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("equipos.id"),
        nullable=True,
    )

    estado_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("estados.id"),
        nullable=True,
    )

    comet_id: Mapped[int | None] = mapped_column(nullable=True)

    hora: Mapped[time | None] = mapped_column(Time, nullable=True)

    cancha_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("canchas.id"),
        nullable=True,
    )

    arbitro_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("arbitros.id"),
        nullable=True,
    )

    goles_local: Mapped[int | None] = mapped_column(
        nullable=True,
        server_default=text("0"),
    )

    goles_visitante: Mapped[int | None] = mapped_column(
        nullable=True,
        server_default=text("0"),
    )

    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    torneo = relationship(
        "Torneos",
        back_populates="partidos",
        foreign_keys=[torneo_id],
    )

    equipo_local = relationship(
        "Equipos",
        back_populates="partidos_locales",
        foreign_keys=[equipo_local_id],
    )

    equipo_visitante = relationship(
        "Equipos",
        back_populates="partidos_visitantes",
        foreign_keys=[equipo_visitante_id],
    )

    cancha = relationship(
        "Canchas",
        back_populates="partidos",
        foreign_keys=[cancha_id],
    )

    arbitro = relationship(
        "Arbitros",
        back_populates="partidos",
        foreign_keys=[arbitro_id],
    )

    estado = relationship(
        "Estados",
        back_populates="partidos",
        foreign_keys=[estado_id],
    )

    partido_jugadores = relationship(
        "PartidoJugadores",
        back_populates="partido",
        cascade="all,delete-orphan",
    )

    archivos_adjuntos = relationship(
        "ArchivosAdjuntos",
        back_populates="partido",
        cascade="all,delete-orphan",
    )

    evaluaciones = relationship(
        "EvaluacionesJugador",
        back_populates="partido",
        cascade="all,delete-orphan",
    )

    formaciones = relationship(
        "Formaciones",
        back_populates="partido",
        cascade="all,delete-orphan",
    )

    videos = relationship(
        "Videos",
        back_populates="partido",
        cascade="all,delete-orphan",
    )
