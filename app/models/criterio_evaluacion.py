from uuid import UUID
import datetime

from sqlalchemy import (
    String,
    Text,
    Boolean,
    DateTime,
    PrimaryKeyConstraint,
    text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CriteriosEvaluacion(Base):

    __tablename__ = "criterios_evaluacion"

    __table_args__ = (
        PrimaryKeyConstraint(
            "id",
            name="criterios_evaluacion_pkey"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text
    )

    activo: Mapped[bool | None] = mapped_column(
        Boolean,
        server_default=text("true")
    )

    created_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )


    evaluaciones_jugador: Mapped[list['EvaluacionesJugador']] = relationship(
        "EvaluacionesJugador",
        back_populates="criterio"
    )
