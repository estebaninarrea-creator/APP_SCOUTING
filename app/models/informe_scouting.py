from uuid import UUID
import datetime

from sqlalchemy import (
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    Index,
    Text,
    DateTime,
    text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class InformesScouting(Base):

    __tablename__ = 'informes_scouting'

    __table_args__ = (
        ForeignKeyConstraint(
            ['jugador_id'],
            ['jugadores.id'],
            name='fk_informe_scouting_jugador'
        ),
        ForeignKeyConstraint(
            ['scout_id'],
            ['scouts.id'],
            name='fk_informe_scouting_scout'
        ),
        PrimaryKeyConstraint(
            'id',
            name='informes_scouting_pkey'
        ),
        Index(
            'idx_informe_scouting_jugador',
            'jugador_id'
        ),
        Index(
            'idx_informe_scouting_scout',
            'scout_id'
        ),
    )


    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()')
    )

    jugador_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False
    )

    scout_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False
    )

    observaciones: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP')
    )


    jugador: Mapped['Jugadores'] = relationship(
        'Jugadores',
        back_populates='informes_scouting'
    )


    scout: Mapped['Scouts'] = relationship(
        'Scouts',
        back_populates='informes_scouting'
    )
