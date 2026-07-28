from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    text
)

from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Equipos(Base):

    __tablename__ = "equipos"


    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )


    club_id: Mapped[UUID] = mapped_column(
        ForeignKey("clubes.id"),
        nullable=False
    )


    temporada_id: Mapped[UUID] = mapped_column(
        ForeignKey("temporadas.id"),
        nullable=False
    )


    categoria_id: Mapped[UUID] = mapped_column(
        ForeignKey("categorias.id"),
        nullable=False
    )


    nombre: Mapped[str | None] = mapped_column(
        String(150)
    )


    director_tecnico: Mapped[str | None] = mapped_column(
        String(150)
    )


    ayudante_tecnico: Mapped[str | None] = mapped_column(
        String(150)
    )


    preparador_fisico: Mapped[str | None] = mapped_column(
        String(150)
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )


    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )


    # =========================
    # Relaciones
    # =========================

    club = relationship(
        "Clubes",
        back_populates="equipos"
    )


    temporada = relationship(
        "Temporadas",
        back_populates="equipos"
    )


    categoria = relationship(
        "Categorias",
        back_populates="equipos"
    )


    planteles = relationship(
        "Planteles",
        back_populates="equipo",
        cascade="all,delete-orphan",
    )


    torneos_clubes = relationship(
        "TorneosClubes",
        back_populates="equipo",
        cascade="all,delete-orphan",
    )

    formaciones = relationship(
        "Formaciones",
        back_populates="equipo",
        cascade="all,delete-orphan",
    )

    partidos_locales = relationship(
        "Partidos",
        back_populates="equipo_local",
        foreign_keys="Partidos.equipo_local_id",
        cascade="all,delete-orphan",
    )

    partidos_visitantes = relationship(
        "Partidos",
        back_populates="equipo_visitante",
        foreign_keys="Partidos.equipo_visitante_id",
        cascade="all,delete-orphan",
    )
