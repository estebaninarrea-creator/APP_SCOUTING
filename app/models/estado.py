from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Estados(Base):
    """
    Tabla de estados de partidos.
    Ejemplos: "Programado", "En curso", "Finalizado", "Cancelado", "Suspendido"
    """
    __tablename__ = "estados"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    descripcion: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Relationships
    partidos = relationship(
        "Partidos",
        back_populates="estado",
        foreign_keys="Partidos.estado_id",
        cascade="all,delete-orphan",
    )
