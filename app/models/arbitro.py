from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Arbitros(Base):
    __tablename__ = "arbitros"

    __table_args__ = (
        Index("idx_arbitro_liga", "liga_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    apellido: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    documento: Mapped[Optional[str]] = mapped_column(
        String(30)
    )

    liga_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ligas.id")
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relaciones
    liga: Mapped[Optional["Ligas"]] = relationship(
        "Ligas",
        back_populates="arbitros"
    )

    partidos = relationship(
        "Partidos",
        back_populates="arbitro",
        foreign_keys="Partidos.arbitro_id",
        cascade="all,delete-orphan",
    )
