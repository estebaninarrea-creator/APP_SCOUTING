from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    CHAR,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Jugadores(Base):
    __tablename__ = "jugadores"

    __table_args__ = (
        CheckConstraint(
            "pierna_habil = ANY (ARRAY['D'::bpchar, 'I'::bpchar, 'A'::bpchar])",
            name="jugadores_pierna_habil_check",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    apellido: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    comet_id: Mapped[int | None] = mapped_column(
        BigInteger
    )

    documento: Mapped[str | None] = mapped_column(
        String(30)
    )

    fecha_nacimiento: Mapped[date | None] = mapped_column(
        Date
    )

    pais_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("paises.id")
    )

    ciudad_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ciudades.id")
    )

    altura: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 2)
    )

    peso: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2)
    )

    pierna_habil: Mapped[str | None] = mapped_column(
        CHAR(1)
    )

    foto_url: Mapped[str | None] = mapped_column(
        Text
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

    ciudad = relationship(
        "Ciudades",
        back_populates="jugadores"
    )

    pais = relationship(
        "Paises",
        back_populates="jugadores"
    )

    informes_scouting = relationship(
        "InformesScouting",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    jugadores_posiciones = relationship(
        "JugadoresPosiciones",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    archivos_adjuntos = relationship(
        "ArchivosAdjuntos",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    planteles = relationship(
        "Planteles",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    evaluaciones = relationship(
        "EvaluacionesJugador",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    partidos = relationship(
        "PartidoJugadores",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    videos = relationship(
        "Videos",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    formaciones = relationship(
        "FormacionJugadores",
        back_populates="jugador",
        cascade="all,delete-orphan",
    )

    @property
    def posiciones(self):
        return [
            {
                "id": item.posicion_id,
                "principal": item.principal or False,
            }
            for item in self.jugadores_posiciones
        ]
