from datetime import datetime
from uuid import UUID

from sqlalchemy import CHAR, CheckConstraint, DateTime, SmallInteger, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Categorias(Base):
    __tablename__ = "categorias"
    __table_args__ = (
        CheckConstraint(
            "sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar, 'X'::bpchar])",
            name="categorias_sexo_check",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    nombre: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        unique=True,
    )

    sexo: Mapped[str] = mapped_column(
        CHAR(1),
        nullable=False,
        server_default=text("'M'::bpchar"),
    )

    edad_min: Mapped[int | None] = mapped_column(
        SmallInteger
    )

    edad_max: Mapped[int | None] = mapped_column(
        SmallInteger
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    equipos = relationship(
        "Equipos",
        back_populates="categoria",
        cascade="all,delete-orphan",
    )

    torneos = relationship(
        "Torneos",
        back_populates="categoria",
        cascade="all,delete-orphan",
    )
