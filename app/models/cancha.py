from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text, text

from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Canchas(Base):

    __tablename__ = "canchas"


    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )


    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )


    # =========================
    # Relaciones
    # =========================

    partidos = relationship(
        "Partidos",
        back_populates="cancha",
        foreign_keys="Partidos.cancha_id",
        cascade="all,delete-orphan",
    )
