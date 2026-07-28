from uuid import UUID

from sqlalchemy import (
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    Index,
    Boolean,
    text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class JugadoresPosiciones(Base):

    __tablename__ = "jugadores_posiciones"

    __table_args__ = (
        ForeignKeyConstraint(
            ["jugador_id"],
            ["jugadores.id"],
            name="fk_jugador_posicion_jugador"
        ),
        ForeignKeyConstraint(
            ["posicion_id"],
            ["posiciones.id"],
            name="fk_jugador_posicion_posicion"
        ),
        PrimaryKeyConstraint(
            "jugador_id",
            "posicion_id",
            name="jugadores_posiciones_pkey"
        ),
        Index(
            "idx_jugador_posicion_jugador",
            "jugador_id"
        ),
        Index(
            "idx_jugador_posicion_posicion",
            "posicion_id"
        ),
    )


    jugador_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        primary_key=True
    )

    posicion_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        primary_key=True
    )

    principal: Mapped[bool | None] = mapped_column(
        Boolean,
        server_default=text("false")
    )

    jugador: Mapped['Jugadores'] = relationship(
        "Jugadores",
        back_populates="jugadores_posiciones"
    )


    posicion: Mapped['Posiciones'] = relationship(
        "Posiciones",
        back_populates="jugadores_posiciones"
    )
