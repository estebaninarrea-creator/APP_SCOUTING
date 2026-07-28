from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Estadios(Base):
    __tablename__ = "estadios"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    club_id: Mapped[UUID] = mapped_column(
        ForeignKey("clubes.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    direccion: Mapped[str | None] = mapped_column(String(200))

    ciudad_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ciudades.id")
    )

    capacidad: Mapped[int | None] = mapped_column(Integer)

    latitud: Mapped[Decimal | None] = mapped_column(
        Numeric(10,7)
    )

    longitud: Mapped[Decimal | None] = mapped_column(
        Numeric(10,7)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    club = relationship(
        "Clubes",
        back_populates="estadios"
    )

    ciudad = relationship(
        "Ciudades",
        back_populates="estadios"
    )

    canchas = relationship(
        "Canchas",
        back_populates="estadio",
        cascade="all,delete-orphan",
    )
