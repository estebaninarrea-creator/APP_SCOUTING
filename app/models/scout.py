from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Scouts(Base):
    __tablename__ = "scouts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    apellido: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    usuario_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("usuarios.id")
    )

    telefono: Mapped[str | None] = mapped_column(
        String(50)
    )

    email: Mapped[str | None] = mapped_column(
        String(150)
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    usuario = relationship(
        "Usuarios",
        back_populates="scouts"
    )

    informes_scouting = relationship(
        "InformesScouting",
        back_populates="scout"
    )

    evaluaciones_jugador = relationship(
        "EvaluacionesJugador",
        back_populates="scout"
    )
