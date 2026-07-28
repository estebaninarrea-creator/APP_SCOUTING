from uuid import UUID

from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FormacionJugadores(Base):
    __tablename__ = "formacion_jugadores"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    formacion_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("formaciones.id"),
        nullable=False
    )

    jugador_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("jugadores.id"),
        nullable=False
    )

    numero_camiseta: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    posicion_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("posiciones.id"),
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "formacion_id",
            "jugador_id",
            name="uq_formacion_jugador"
        ),
    )

    # Relationships
    formacion = relationship(
        "Formaciones",
        back_populates="jugadores"
    )

    jugador = relationship(
        "Jugadores",
        back_populates="formaciones"
    )

    posicion = relationship(
        "Posiciones",
        back_populates="formacion_jugadores"
    )
