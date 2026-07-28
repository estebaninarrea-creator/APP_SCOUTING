from datetime import datetime
from uuid import UUID

from sqlalchemy import CHAR, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Paises(Base):
    __tablename__ = "paises"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    codigo_iso2: Mapped[str] = mapped_column(
        CHAR(2),
        nullable=False,
        unique=True
    )

    codigo_iso3: Mapped[str | None] = mapped_column(
        CHAR(3)
    )

    codigo_fifa: Mapped[str | None] = mapped_column(
        CHAR(3)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    provincias = relationship("Provincias", back_populates="pais", cascade="all,delete-orphan")

    ligas = relationship("Ligas", back_populates="pais", cascade="all,delete-orphan")

    jugadores = relationship("Jugadores", back_populates="pais", cascade="all,delete-orphan")
