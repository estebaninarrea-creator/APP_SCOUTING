from uuid import UUID
import datetime

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    String,
    text
)

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PartidoJugadores(Base):

    __tablename__ = "partido_jugadores"


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


    jugador_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("jugadores.id"),
        nullable=False
    )


    numero_camiseta: Mapped[int | None] = mapped_column(
        Integer
    )


    posicion: Mapped[str | None] = mapped_column(
        String(50)
    )


    minutos_jugados: Mapped[int | None] = mapped_column(
        Integer
    )


    created_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )


    # Relaciones
    partido: Mapped["Partidos"] = relationship(
        "Partidos",
        back_populates="partido_jugadores"
    )

    jugador: Mapped["Jugadores"] = relationship(
        "Jugadores",
        back_populates="partidos"
    )    
