from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, SmallInteger, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Planteles(Base):
    __tablename__ = "planteles"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    equipo_id: Mapped[UUID] = mapped_column(
        ForeignKey("equipos.id"),
        nullable=False
    )

    jugador_id: Mapped[UUID] = mapped_column(
        ForeignKey("jugadores.id"),
        nullable=False
    )

    fecha_desde: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    dorsal: Mapped[int | None] = mapped_column(SmallInteger)

    fecha_hasta: Mapped[date | None] = mapped_column(Date)

    activo: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    equipo = relationship(
        "Equipos",
        back_populates="planteles"
    )

    jugador = relationship(
        "Jugadores",
        back_populates="planteles"
    )
