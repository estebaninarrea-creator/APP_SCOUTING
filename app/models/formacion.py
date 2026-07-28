from uuid import UUID
import datetime

from sqlalchemy import ForeignKey, DateTime, Text, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Formaciones(Base):

    __tablename__ = "formaciones"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    partido_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("partidos.id"),
        nullable=False
    )

    equipo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("equipos.id"),
        nullable=False
    )

    esquema: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )


    partido: Mapped["Partidos"] = relationship(
        "Partidos",
        back_populates="formaciones"
    )

    equipo: Mapped["Equipos"] = relationship(
        "Equipos",
        back_populates="formaciones"
    )

    jugadores = relationship(
        "FormacionJugadores",
        back_populates="formacion"
    )

