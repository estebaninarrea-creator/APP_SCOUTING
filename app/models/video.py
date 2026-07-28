from uuid import UUID

from sqlalchemy import (
    Text,
    DateTime,
    ForeignKeyConstraint,
    text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Videos(Base):
    __tablename__ = "videos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    jugador_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False
    )

    partido_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    fecha_carga: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=text("now()")
    )


    __table_args__ = (
        ForeignKeyConstraint(
            ["jugador_id"],
            ["jugadores.id"],
            name="fk_video_jugador"
        ),
        ForeignKeyConstraint(
            ["partido_id"],
            ["partidos.id"],
            name="fk_video_partido"
        ),
    )


    jugador = relationship(
        "Jugadores",
        back_populates="videos"
    )

    partido = relationship(
        "Partidos",
        back_populates="videos"
    )
    
