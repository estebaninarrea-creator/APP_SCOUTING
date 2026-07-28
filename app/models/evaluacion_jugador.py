from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class EvaluacionesJugador(Base):
    __tablename__ = "evaluaciones_jugador"

    __table_args__ = (
        CheckConstraint(
            "valor >= 1 AND valor <= 10",
            name="chk_valor_evaluacion",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    jugador_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("jugadores.id"),
        nullable=False,
    )

    partido_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("partidos.id"),
        nullable=False,
    )

    scout_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("scouts.id"),
        nullable=False,
    )

    criterio_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("criterios_evaluacion.id"),
        nullable=False,
    )

    valor: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comentario: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # =========================
    # Relaciones
    # =========================

    jugador = relationship(
        "Jugadores",
        back_populates="evaluaciones",
    )

    partido = relationship(
        "Partidos",
        back_populates="evaluaciones",
    )

    scout = relationship(
        "Scouts",
        back_populates="evaluaciones_jugador",
    )

    criterio = relationship(
        "CriteriosEvaluacion",
        back_populates="evaluaciones_jugador",
    )
