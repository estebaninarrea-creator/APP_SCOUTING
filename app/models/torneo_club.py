from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TorneosClubes(Base):
    __tablename__ = "torneos_clubes"

    torneo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("torneos.id"),
        primary_key=True
    )

    equipo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("equipos.id"),
        primary_key=True
    )

    zona: Mapped[str | None]

    grupo: Mapped[str | None]

    torneo = relationship(
        "Torneos",
        back_populates="torneos_clubes"
    )

    equipo = relationship(
        "Equipos",
        back_populates="torneos_clubes"
    )
