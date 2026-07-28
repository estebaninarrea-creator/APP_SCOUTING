from uuid import UUID

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    Index,
    text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ArchivosAdjuntos(Base):
    __tablename__ = "archivos_adjuntos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    jugador_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True
    )

    partido_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True
    )

    nombre_archivo: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ruta_archivo: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    tipo_archivo: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    fecha_carga: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=text("now()")
    )


    __table_args__ = (
        PrimaryKeyConstraint(
            "id",
            name="archivos_adjuntos_pkey"
        ),

        ForeignKeyConstraint(
            ["jugador_id"],
            ["jugadores.id"],
            name="fk_archivo_jugador"
        ),

        ForeignKeyConstraint(
            ["partido_id"],
            ["partidos.id"],
            name="fk_archivo_partido"
        ),

        Index(
            "idx_archivo_jugador",
            "jugador_id"
        ),

        Index(
            "idx_archivo_partido",
            "partido_id"
        ),
    )


    jugador = relationship(
        "Jugadores",
        back_populates="archivos_adjuntos"
    )

    partido = relationship(
        "Partidos",
        back_populates="archivos_adjuntos"
    )
