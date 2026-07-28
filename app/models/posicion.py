from uuid import UUID

from sqlalchemy import SmallInteger, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Posiciones(Base):
    __tablename__ = "posiciones"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    codigo: Mapped[str] = mapped_column(String(10), nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    orden: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default=text("1"))

    __table_args__ = (
        UniqueConstraint(
            'codigo',
            name='posiciones_codigo_key'
        ),
    )

    jugadores_posiciones = relationship(
        "JugadoresPosiciones",
        back_populates="posicion",
        cascade="all,delete-orphan",
    )

    formacion_jugadores = relationship(
        "FormacionJugadores",
        back_populates="posicion",
        cascade="all,delete-orphan",
    )
