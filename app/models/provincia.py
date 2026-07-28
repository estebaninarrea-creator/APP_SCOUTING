from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Provincias(Base):
    __tablename__ = "provincias"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    pais_id: Mapped[UUID] = mapped_column(
        ForeignKey("paises.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    pais = relationship(
        "Paises",
        back_populates="provincias"
    )

    ciudades = relationship(
        "Ciudades",
        back_populates="provincia",
        cascade="all,delete-orphan",
    )

    ligas = relationship(
        "Ligas",
        back_populates="provincia",
        cascade="all,delete-orphan",
    )
