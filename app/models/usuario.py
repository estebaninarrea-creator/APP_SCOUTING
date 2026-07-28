from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Usuarios(Base):
    __tablename__ = "usuarios"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    rol_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    apellido: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    rol = relationship(
        "Roles",
        back_populates="usuarios"
    )

    ligas = relationship(
        "Ligas",
        secondary="usuarios_ligas",
        back_populates="usuarios"
    )

    scouts = relationship(
        "Scouts",
        back_populates="usuario",
        cascade="all,delete-orphan",
    )
