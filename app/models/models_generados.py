from typing import Optional
import datetime
import decimal
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, CHAR, CheckConstraint, Column, Date, DateTime, Double, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Table, Text, Time, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import OID, UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Categorias(Base):
    __tablename__ = 'categorias'
    __table_args__ = (
        CheckConstraint("sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar, 'X'::bpchar])", name='categorias_sexo_check'),
        PrimaryKeyConstraint('id', name='categorias_pkey'),
        UniqueConstraint('nombre', name='categorias_nombre_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    sexo: Mapped[str] = mapped_column(CHAR(1), nullable=False, server_default=text("'M'::bpchar"))
    edad_min: Mapped[Optional[int]] = mapped_column(SmallInteger)
    edad_max: Mapped[Optional[int]] = mapped_column(SmallInteger)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    equipos: Mapped[list['Equipos']] = relationship('Equipos', back_populates='categoria')
    torneos: Mapped[list['Torneos']] = relationship('Torneos', back_populates='categoria')


class CriteriosEvaluacion(Base):
    __tablename__ = 'criterios_evaluacion'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='criterios_evaluacion_pkey'),
        UniqueConstraint('codigo', name='criterios_evaluacion_codigo_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    valor_min: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('1'))
    valor_max: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('10'))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    evaluaciones_jugador: Mapped[list['EvaluacionesJugador']] = relationship('EvaluacionesJugador', back_populates='criterio')


class EstadosPartido(Base):
    __tablename__ = 'estados_partido'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='estados_partido_pkey'),
        UniqueConstraint('codigo', name='estados_partido_codigo_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    codigo: Mapped[str] = mapped_column(String(30), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    partidos: Mapped[list['Partidos']] = relationship('Partidos', back_populates='estado')


class Paises(Base):
    __tablename__ = 'paises'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='paises_pkey'),
        UniqueConstraint('codigo_iso2', name='paises_codigo_iso2_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_iso2: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    codigo_iso3: Mapped[Optional[str]] = mapped_column(CHAR(3))
    codigo_fifa: Mapped[Optional[str]] = mapped_column(CHAR(3))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    provincias: Mapped[list['Provincias']] = relationship('Provincias', back_populates='pais')
    ligas: Mapped[list['Ligas']] = relationship('Ligas', back_populates='pais')
    jugadores: Mapped[list['Jugadores']] = relationship('Jugadores', back_populates='pais')


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('shared_blk_read_time', Double(53)),
    Column('shared_blk_write_time', Double(53)),
    Column('local_blk_read_time', Double(53)),
    Column('local_blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53)),
    Column('jit_deform_count', BigInteger),
    Column('jit_deform_time', Double(53)),
    Column('stats_since', DateTime(True)),
    Column('minmax_stats_since', DateTime(True))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


class PiernasHabiles(Base):
    __tablename__ = 'piernas_habiles'
    __table_args__ = (
        PrimaryKeyConstraint('codigo', name='piernas_habiles_pkey'),
    )

    codigo: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    descripcion: Mapped[str] = mapped_column(String(50), nullable=False)


class Posiciones(Base):
    __tablename__ = 'posiciones'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='posiciones_pkey'),
        UniqueConstraint('codigo', name='posiciones_codigo_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    codigo: Mapped[str] = mapped_column(String(10), nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    orden: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    jugadores_posiciones: Mapped[list['JugadoresPosiciones']] = relationship('JugadoresPosiciones', back_populates='posicion')
    partido_jugadores: Mapped[list['PartidoJugadores']] = relationship('PartidoJugadores', back_populates='posicion')
    formacion_jugadores: Mapped[list['FormacionJugadores']] = relationship('FormacionJugadores', back_populates='posicion')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='roles_pkey'),
        UniqueConstraint('nombre', name='roles_nombre_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(String(200))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    usuarios: Mapped[list['Usuarios']] = relationship('Usuarios', back_populates='rol')


class TiposSuperficie(Base):
    __tablename__ = 'tipos_superficie'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tipos_superficie_pkey'),
        UniqueConstraint('nombre', name='tipos_superficie_nombre_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)


class TiposTorneo(Base):
    __tablename__ = 'tipos_torneo'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tipos_torneo_pkey'),
        UniqueConstraint('nombre', name='tipos_torneo_nombre_key')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    torneos: Mapped[list['Torneos']] = relationship('Torneos', back_populates='tipo_torneo')


t_vw_evaluaciones_jugador = Table(
    'vw_evaluaciones_jugador', Base.metadata,
    Column('jugador_id', PG_UUID(as_uuid=True)),
    Column('nombre', String(120)),
    Column('apellido', String(120)),
    Column('criterio', String(100)),
    Column('valor', SmallInteger),
    Column('comentario', Text),
    Column('scout', String(120)),
    Column('scout_apellido', String(120)),
    Column('created_at', DateTime)
)


t_vw_fixture_torneo = Table(
    'vw_fixture_torneo', Base.metadata,
    Column('partido_id', PG_UUID(as_uuid=True)),
    Column('torneo', String(150)),
    Column('fecha', Date),
    Column('hora', Time),
    Column('local', String(150)),
    Column('visitante', String(150)),
    Column('goles_local', SmallInteger),
    Column('goles_visitante', SmallInteger),
    Column('estado', String(100))
)


t_vw_historial_jugador = Table(
    'vw_historial_jugador', Base.metadata,
    Column('jugador_id', PG_UUID(as_uuid=True)),
    Column('nombre', String(120)),
    Column('apellido', String(120)),
    Column('club', String(150)),
    Column('equipo', String(150)),
    Column('categoria', String(60)),
    Column('fecha_desde', Date),
    Column('fecha_hasta', Date)
)


t_vw_jugador_partidos = Table(
    'vw_jugador_partidos', Base.metadata,
    Column('jugador_id', PG_UUID(as_uuid=True)),
    Column('nombre', String(120)),
    Column('apellido', String(120)),
    Column('fecha', Date),
    Column('equipo', String(150)),
    Column('titular', Boolean),
    Column('capitan', Boolean),
    Column('numero_camiseta', SmallInteger),
    Column('posicion', String(80)),
    Column('minutos_jugados', SmallInteger)
)


t_vw_jugadores = Table(
    'vw_jugadores', Base.metadata,
    Column('id', PG_UUID(as_uuid=True)),
    Column('apellido', String(120)),
    Column('nombre', String(120)),
    Column('jugador', Text),
    Column('fecha_nacimiento', Date),
    Column('edad', Numeric),
    Column('pais', String(100)),
    Column('ciudad', String(120)),
    Column('altura', Numeric(4, 2)),
    Column('peso', Numeric(5, 2)),
    Column('pierna_habil', CHAR(1)),
    Column('foto_url', Text),
    Column('activo', Boolean)
)


t_vw_planteles_actuales = Table(
    'vw_planteles_actuales', Base.metadata,
    Column('plantel_id', PG_UUID(as_uuid=True)),
    Column('equipo_id', PG_UUID(as_uuid=True)),
    Column('club', String(150)),
    Column('equipo', String(150)),
    Column('categoria', String(60)),
    Column('jugador_id', PG_UUID(as_uuid=True)),
    Column('nombre', String(120)),
    Column('apellido', String(120)),
    Column('dorsal', SmallInteger),
    Column('fecha_desde', Date)
)


t_vw_potencial_jugadores = Table(
    'vw_potencial_jugadores', Base.metadata,
    Column('id', PG_UUID(as_uuid=True)),
    Column('nombre', String(120)),
    Column('apellido', String(120)),
    Column('promedio_evaluacion', Numeric),
    Column('cantidad_evaluaciones', BigInteger)
)


class Provincias(Base):
    __tablename__ = 'provincias'
    __table_args__ = (
        ForeignKeyConstraint(['pais_id'], ['paises.id'], name='fk_provincia_pais'),
        PrimaryKeyConstraint('id', name='provincias_pkey'),
        Index('idx_provincia_pais', 'pais_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    pais_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    pais: Mapped['Paises'] = relationship('Paises', back_populates='provincias')
    ciudades: Mapped[list['Ciudades']] = relationship('Ciudades', back_populates='provincia')
    ligas: Mapped[list['Ligas']] = relationship('Ligas', back_populates='provincia')


class Usuarios(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        ForeignKeyConstraint(['rol_id'], ['roles.id'], name='fk_usuario_rol'),
        PrimaryKeyConstraint('id', name='usuarios_pkey'),
        UniqueConstraint('email', name='usuarios_email_key'),
        Index('idx_usuario_activo', 'activo'),
        Index('idx_usuario_nombre', 'apellido', 'nombre'),
        Index('idx_usuarios_email', 'email')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    rol_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    rol: Mapped['Roles'] = relationship('Roles', back_populates='usuarios')
    liga: Mapped[list['Ligas']] = relationship('Ligas', secondary='usuarios_ligas', back_populates='usuario')
    scouts: Mapped[list['Scouts']] = relationship('Scouts', back_populates='usuario')


class Ciudades(Base):
    __tablename__ = 'ciudades'
    __table_args__ = (
        ForeignKeyConstraint(['provincia_id'], ['provincias.id'], name='fk_ciudad_provincia'),
        PrimaryKeyConstraint('id', name='ciudades_pkey'),
        Index('idx_ciudad_provincia', 'provincia_id'),
        Index('idx_ciudades_nombre', 'nombre')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    provincia_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    codigo_postal: Mapped[Optional[str]] = mapped_column(String(20))
    latitud: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 7))
    longitud: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 7))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    provincia: Mapped['Provincias'] = relationship('Provincias', back_populates='ciudades')
    clubes: Mapped[list['Clubes']] = relationship('Clubes', back_populates='ciudad')
    jugadores: Mapped[list['Jugadores']] = relationship('Jugadores', back_populates='ciudad')
    estadios: Mapped[list['Estadios']] = relationship('Estadios', back_populates='ciudad')


class Ligas(Base):
    __tablename__ = 'ligas'
    __table_args__ = (
        ForeignKeyConstraint(['pais_id'], ['paises.id'], name='fk_liga_pais'),
        ForeignKeyConstraint(['provincia_id'], ['provincias.id'], name='fk_liga_provincia'),
        PrimaryKeyConstraint('id', name='ligas_pkey'),
        Index('idx_liga_activa', 'activo'),
        Index('idx_liga_pais', 'pais_id'),
        Index('idx_liga_provincia', 'provincia_id'),
        Index('idx_ligas_nombre', 'nombre')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    comet_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    pais_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    provincia_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    logo_url: Mapped[Optional[str]] = mapped_column(Text)
    sitio_web: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(String(150))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    pais: Mapped[Optional['Paises']] = relationship('Paises', back_populates='ligas')
    provincia: Mapped[Optional['Provincias']] = relationship('Provincias', back_populates='ligas')
    usuario: Mapped[list['Usuarios']] = relationship('Usuarios', secondary='usuarios_ligas', back_populates='liga')
    arbitros: Mapped[list['Arbitros']] = relationship('Arbitros', back_populates='liga')
    temporadas: Mapped[list['Temporadas']] = relationship('Temporadas', back_populates='liga')


class Scouts(Base):
    __tablename__ = 'scouts'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], name='fk_scout_usuario'),
        PrimaryKeyConstraint('id', name='scouts_pkey'),
        Index('idx_scout_usuario', 'usuario_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    usuario_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(150))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    usuario: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='scouts')
    informes_scouting: Mapped[list['InformesScouting']] = relationship('InformesScouting', back_populates='scout')
    evaluaciones_jugador: Mapped[list['EvaluacionesJugador']] = relationship('EvaluacionesJugador', back_populates='scout')


class Arbitros(Base):
    __tablename__ = 'arbitros'
    __table_args__ = (
        ForeignKeyConstraint(['liga_id'], ['ligas.id'], name='fk_arbitro_liga'),
        PrimaryKeyConstraint('id', name='arbitros_pkey'),
        Index('idx_arbitro_liga', 'liga_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    documento: Mapped[Optional[str]] = mapped_column(String(30))
    liga_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    liga: Mapped[Optional['Ligas']] = relationship('Ligas', back_populates='arbitros')
    partidos: Mapped[list['Partidos']] = relationship('Partidos', back_populates='arbitro')


class Clubes(Base):
    __tablename__ = 'clubes'
    __table_args__ = (
        ForeignKeyConstraint(['ciudad_id'], ['ciudades.id'], name='fk_club_ciudad'),
        PrimaryKeyConstraint('id', name='clubes_pkey'),
        Index('idx_club_ciudad', 'ciudad_id'),
        Index('idx_club_comet', 'comet_id'),
        Index('idx_club_nombre', 'nombre', unique=True),
        {'comment': 'Instituciones deportivas. Un club puede tener m�ltiples equipos y '
                'categor�as.'}
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    comet_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    nombre_corto: Mapped[Optional[str]] = mapped_column(String(50))
    sigla: Mapped[Optional[str]] = mapped_column(String(10))
    ciudad_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(150))
    sitio_web: Mapped[Optional[str]] = mapped_column(Text)
    escudo_url: Mapped[Optional[str]] = mapped_column(Text)
    fundacion: Mapped[Optional[datetime.date]] = mapped_column(Date)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    ciudad: Mapped[Optional['Ciudades']] = relationship('Ciudades', back_populates='clubes')
    equipos: Mapped[list['Equipos']] = relationship('Equipos', back_populates='club')
    estadios: Mapped[list['Estadios']] = relationship('Estadios', back_populates='club')


class Jugadores(Base):
    __tablename__ = 'jugadores'
    __table_args__ = (
        CheckConstraint("pierna_habil = ANY (ARRAY['D'::bpchar, 'I'::bpchar, 'A'::bpchar])", name='jugadores_pierna_habil_check'),
        ForeignKeyConstraint(['ciudad_id'], ['ciudades.id'], name='fk_jugador_ciudad'),
        ForeignKeyConstraint(['pais_id'], ['paises.id'], name='fk_jugador_pais'),
        PrimaryKeyConstraint('id', name='jugadores_pkey'),
        Index('idx_jugador_apellido', 'apellido'),
        Index('idx_jugador_apellido_lower'),
        Index('idx_jugador_comet', 'comet_id'),
        Index('idx_jugador_fecha_nacimiento', 'fecha_nacimiento'),
        Index('idx_jugador_nombre', 'apellido', 'nombre'),
        Index('idx_jugador_pais', 'pais_id'),
        {'comment': 'Registro maestro de jugadores independientemente del club actual.'}
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    comet_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    documento: Mapped[Optional[str]] = mapped_column(String(30))
    fecha_nacimiento: Mapped[Optional[datetime.date]] = mapped_column(Date)
    pais_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    ciudad_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    altura: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2))
    peso: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    pierna_habil: Mapped[Optional[str]] = mapped_column(CHAR(1))
    foto_url: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    ciudad: Mapped[Optional['Ciudades']] = relationship('Ciudades', back_populates='jugadores')
    pais: Mapped[Optional['Paises']] = relationship('Paises', back_populates='jugadores')
    informes_scouting: Mapped[list['InformesScouting']] = relationship('InformesScouting', back_populates='jugador')
    jugadores_posiciones: Mapped[list['JugadoresPosiciones']] = relationship('JugadoresPosiciones', back_populates='jugador')
    archivos_adjuntos: Mapped[list['ArchivosAdjuntos']] = relationship('ArchivosAdjuntos', back_populates='jugador')
    planteles: Mapped[list['Planteles']] = relationship('Planteles', back_populates='jugador')
    evaluaciones_jugador: Mapped[list['EvaluacionesJugador']] = relationship('EvaluacionesJugador', back_populates='jugador')
    partido_jugadores: Mapped[list['PartidoJugadores']] = relationship('PartidoJugadores', back_populates='jugador')
    videos: Mapped[list['Videos']] = relationship('Videos', back_populates='jugador')
    formacion_jugadores: Mapped[list['FormacionJugadores']] = relationship('FormacionJugadores', back_populates='jugador')


class Temporadas(Base):
    __tablename__ = 'temporadas'
    __table_args__ = (
        ForeignKeyConstraint(['liga_id'], ['ligas.id'], name='fk_temporada_liga'),
        PrimaryKeyConstraint('id', name='temporadas_pkey'),
        UniqueConstraint('liga_id', 'nombre', name='uk_temporada'),
        Index('idx_temporada_activa', 'activa'),
        Index('idx_temporada_liga', 'liga_id'),
        Index('idx_temporadas_nombre', 'nombre')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    liga_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    fecha_inicio: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    activa: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    liga: Mapped['Ligas'] = relationship('Ligas', back_populates='temporadas')
    equipos: Mapped[list['Equipos']] = relationship('Equipos', back_populates='temporada')
    torneos: Mapped[list['Torneos']] = relationship('Torneos', back_populates='temporada')


t_usuarios_ligas = Table(
    'usuarios_ligas', Base.metadata,
    Column('usuario_id', PG_UUID(as_uuid=True), primary_key=True),
    Column('liga_id', PG_UUID(as_uuid=True), primary_key=True),
    ForeignKeyConstraint(['liga_id'], ['ligas.id'], name='fk_ul_liga'),
    ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], name='fk_ul_usuario'),
    PrimaryKeyConstraint('usuario_id', 'liga_id', name='usuarios_ligas_pkey')
)


class Equipos(Base):
    __tablename__ = 'equipos'
    __table_args__ = (
        ForeignKeyConstraint(['categoria_id'], ['categorias.id'], name='fk_equipo_categoria'),
        ForeignKeyConstraint(['club_id'], ['clubes.id'], name='fk_equipo_club'),
        ForeignKeyConstraint(['temporada_id'], ['temporadas.id'], name='fk_equipo_temporada'),
        PrimaryKeyConstraint('id', name='equipos_pkey'),
        UniqueConstraint('club_id', 'temporada_id', 'categoria_id', name='uk_equipo'),
        Index('idx_equipo_busqueda', 'club_id', 'temporada_id', 'categoria_id'),
        Index('idx_equipo_categoria', 'categoria_id'),
        Index('idx_equipo_club', 'club_id'),
        Index('idx_equipo_temporada', 'temporada_id'),
        {'comment': 'Planteles deportivos asociados a una categor�a y temporada.'}
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    club_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    temporada_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    categoria_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[Optional[str]] = mapped_column(String(150))
    director_tecnico: Mapped[Optional[str]] = mapped_column(String(150))
    ayudante_tecnico: Mapped[Optional[str]] = mapped_column(String(150))
    preparador_fisico: Mapped[Optional[str]] = mapped_column(String(150))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    categoria: Mapped['Categorias'] = relationship('Categorias', back_populates='equipos')
    club: Mapped['Clubes'] = relationship('Clubes', back_populates='equipos')
    temporada: Mapped['Temporadas'] = relationship('Temporadas', back_populates='equipos')
    planteles: Mapped[list['Planteles']] = relationship('Planteles', back_populates='equipo')
    torneos_clubes: Mapped[list['TorneosClubes']] = relationship('TorneosClubes', back_populates='equipo')
    partidos_local_equipo: Mapped[list['Partidos']] = relationship('Partidos', foreign_keys='[Partidos.local_equipo_id]', back_populates='local_equipo')
    partidos_visitante_equipo: Mapped[list['Partidos']] = relationship('Partidos', foreign_keys='[Partidos.visitante_equipo_id]', back_populates='visitante_equipo')
    formaciones: Mapped[list['Formaciones']] = relationship('Formaciones', back_populates='equipo')
    partido_jugadores: Mapped[list['PartidoJugadores']] = relationship('PartidoJugadores', back_populates='equipo')


class Estadios(Base):
    __tablename__ = 'estadios'
    __table_args__ = (
        ForeignKeyConstraint(['ciudad_id'], ['ciudades.id'], name='fk_estadio_ciudad'),
        ForeignKeyConstraint(['club_id'], ['clubes.id'], name='fk_estadio_club'),
        PrimaryKeyConstraint('id', name='estadios_pkey')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    club_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    ciudad_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    capacidad: Mapped[Optional[int]] = mapped_column(Integer)
    latitud: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 7))
    longitud: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 7))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    ciudad: Mapped[Optional['Ciudades']] = relationship('Ciudades', back_populates='estadios')
    club: Mapped['Clubes'] = relationship('Clubes', back_populates='estadios')
    canchas: Mapped[list['Canchas']] = relationship('Canchas', back_populates='estadio')


class InformesScouting(Base):
    __tablename__ = 'informes_scouting'
    __table_args__ = (
        CheckConstraint('potencial >= 1 AND potencial <= 10', name='chk_potencial'),
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_informe_jugador'),
        ForeignKeyConstraint(['scout_id'], ['scouts.id'], name='fk_informe_scout'),
        PrimaryKeyConstraint('id', name='informes_scouting_pkey'),
        Index('idx_informe_jugador', 'jugador_id'),
        Index('idx_informe_scout', 'scout_id'),
        {'comment': 'Informes cualitativos realizados por scouts.'}
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    jugador_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    scout_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    titulo: Mapped[Optional[str]] = mapped_column(String(200))
    resumen: Mapped[Optional[str]] = mapped_column(Text)
    fortalezas: Mapped[Optional[str]] = mapped_column(Text)
    debilidades: Mapped[Optional[str]] = mapped_column(Text)
    recomendacion: Mapped[Optional[str]] = mapped_column(Text)
    potencial: Mapped[Optional[int]] = mapped_column(SmallInteger)
    fecha: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('CURRENT_DATE'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    jugador: Mapped['Jugadores'] = relationship('Jugadores', back_populates='informes_scouting')
    scout: Mapped[Optional['Scouts']] = relationship('Scouts', back_populates='informes_scouting')
    archivos_adjuntos: Mapped[list['ArchivosAdjuntos']] = relationship('ArchivosAdjuntos', back_populates='informe')


class JugadoresPosiciones(Base):
    __tablename__ = 'jugadores_posiciones'
    __table_args__ = (
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_jp_jugador'),
        ForeignKeyConstraint(['posicion_id'], ['posiciones.id'], name='fk_jp_posicion'),
        PrimaryKeyConstraint('jugador_id', 'posicion_id', name='jugadores_posiciones_pkey'),
        Index('idx_jugador_posicion_jugador', 'jugador_id'),
        Index('idx_jugador_posicion_posicion', 'posicion_id')
    )

    jugador_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    posicion_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    principal: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    prioridad: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('1'))

    jugador: Mapped['Jugadores'] = relationship('Jugadores', back_populates='jugadores_posiciones')
    posicion: Mapped['Posiciones'] = relationship('Posiciones', back_populates='jugadores_posiciones')


class Torneos(Base):
    __tablename__ = 'torneos'
    __table_args__ = (
        ForeignKeyConstraint(['categoria_id'], ['categorias.id'], name='fk_torneo_categoria'),
        ForeignKeyConstraint(['temporada_id'], ['temporadas.id'], name='fk_torneo_temporada'),
        ForeignKeyConstraint(['tipo_torneo_id'], ['tipos_torneo.id'], name='fk_torneo_tipo'),
        PrimaryKeyConstraint('id', name='torneos_pkey'),
        Index('idx_torneo_activo', 'activo'),
        Index('idx_torneo_categoria', 'categoria_id'),
        Index('idx_torneo_temporada', 'temporada_id'),
        Index('idx_torneos_nombre', 'nombre')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    temporada_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    categoria_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    tipo_torneo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    comet_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    fecha_inicio: Mapped[Optional[datetime.date]] = mapped_column(Date)
    fecha_fin: Mapped[Optional[datetime.date]] = mapped_column(Date)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    categoria: Mapped['Categorias'] = relationship('Categorias', back_populates='torneos')
    temporada: Mapped['Temporadas'] = relationship('Temporadas', back_populates='torneos')
    tipo_torneo: Mapped['TiposTorneo'] = relationship('TiposTorneo', back_populates='torneos')
    torneos_clubes: Mapped[list['TorneosClubes']] = relationship('TorneosClubes', back_populates='torneo')
    partidos: Mapped[list['Partidos']] = relationship('Partidos', back_populates='torneo')


class ArchivosAdjuntos(Base):
    __tablename__ = 'archivos_adjuntos'
    __table_args__ = (
        ForeignKeyConstraint(['informe_id'], ['informes_scouting.id'], name='fk_archivo_informe'),
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_archivo_jugador'),
        PrimaryKeyConstraint('id', name='archivos_adjuntos_pkey'),
        Index('idx_archivo_jugador', 'jugador_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    ruta: Mapped[str] = mapped_column(Text, nullable=False)
    jugador_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    informe_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    nombre_archivo: Mapped[Optional[str]] = mapped_column(String(255))
    extension: Mapped[Optional[str]] = mapped_column(String(20))
    tama�o: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    informe: Mapped[Optional['InformesScouting']] = relationship('InformesScouting', back_populates='archivos_adjuntos')
    jugador: Mapped[Optional['Jugadores']] = relationship('Jugadores', back_populates='archivos_adjuntos')


class Canchas(Base):
    __tablename__ = 'canchas'
    __table_args__ = (
        ForeignKeyConstraint(['estadio_id'], ['estadios.id'], name='fk_cancha_estadio'),
        PrimaryKeyConstraint('id', name='canchas_pkey')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    estadio_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_superficie: Mapped[Optional[str]] = mapped_column(String(30))
    iluminacion: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    habilitada: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    estadio: Mapped['Estadios'] = relationship('Estadios', back_populates='canchas')
    partidos: Mapped[list['Partidos']] = relationship('Partidos', back_populates='cancha')


class Planteles(Base):
    __tablename__ = 'planteles'
    __table_args__ = (
        ForeignKeyConstraint(['equipo_id'], ['equipos.id'], name='fk_plantel_equipo'),
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_plantel_jugador'),
        PrimaryKeyConstraint('id', name='planteles_pkey'),
        Index('idx_plantel_equipo', 'equipo_id'),
        Index('idx_plantel_equipo_activo', 'equipo_id', 'activo'),
        Index('idx_plantel_historial', 'jugador_id', 'fecha_desde', 'fecha_hasta'),
        Index('idx_plantel_jugador', 'jugador_id'),
        Index('idx_plantel_jugador_activo', 'jugador_id', 'activo'),
        {'comment': 'Historial de pertenencia de jugadores a equipos.'}
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    equipo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    jugador_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    fecha_desde: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    dorsal: Mapped[Optional[int]] = mapped_column(SmallInteger)
    fecha_hasta: Mapped[Optional[datetime.date]] = mapped_column(Date)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    equipo: Mapped['Equipos'] = relationship('Equipos', back_populates='planteles')
    jugador: Mapped['Jugadores'] = relationship('Jugadores', back_populates='planteles')


class TorneosClubes(Base):
    __tablename__ = 'torneos_clubes'
    __table_args__ = (
        ForeignKeyConstraint(['equipo_id'], ['equipos.id'], name='fk_tc_equipo'),
        ForeignKeyConstraint(['torneo_id'], ['torneos.id'], name='fk_tc_torneo'),
        PrimaryKeyConstraint('torneo_id', 'equipo_id', name='torneos_clubes_pkey'),
        Index('idx_tc_equipo', 'equipo_id'),
        Index('idx_tc_torneo', 'torneo_id')
    )

    torneo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    equipo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    zona: Mapped[Optional[str]] = mapped_column(String(30))
    grupo: Mapped[Optional[str]] = mapped_column(String(30))

    equipo: Mapped['Equipos'] = relationship('Equipos', back_populates='torneos_clubes')
    torneo: Mapped['Torneos'] = relationship('Torneos', back_populates='torneos_clubes')


class Partidos(Base):
    __tablename__ = 'partidos'
    __table_args__ = (
        CheckConstraint('local_equipo_id <> visitante_equipo_id', name='chk_equipos_distintos'),
        ForeignKeyConstraint(['arbitro_id'], ['arbitros.id'], name='fk_partido_arbitro'),
        ForeignKeyConstraint(['cancha_id'], ['canchas.id'], name='fk_partido_cancha'),
        ForeignKeyConstraint(['estado_id'], ['estados_partido.id'], name='fk_partido_estado'),
        ForeignKeyConstraint(['local_equipo_id'], ['equipos.id'], name='fk_partido_local'),
        ForeignKeyConstraint(['torneo_id'], ['torneos.id'], name='fk_partido_torneo'),
        ForeignKeyConstraint(['visitante_equipo_id'], ['equipos.id'], name='fk_partido_visitante'),
        PrimaryKeyConstraint('id', name='partidos_pkey'),
        Index('idx_partido_estado', 'estado_id'),
        Index('idx_partido_fecha', 'fecha'),
        Index('idx_partido_local', 'local_equipo_id'),
        Index('idx_partido_torneo', 'torneo_id'),
        Index('idx_partido_torneo_fecha', 'torneo_id', 'fecha'),
        Index('idx_partido_visitante', 'visitante_equipo_id'),
        {'comment': 'Encuentros oficiales dentro de un torneo.'}
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    torneo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    local_equipo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    visitante_equipo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    estado_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    comet_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    hora: Mapped[Optional[datetime.time]] = mapped_column(Time)
    cancha_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    arbitro_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    goles_local: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    goles_visitante: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    arbitro: Mapped[Optional['Arbitros']] = relationship('Arbitros', back_populates='partidos')
    cancha: Mapped[Optional['Canchas']] = relationship('Canchas', back_populates='partidos')
    estado: Mapped['EstadosPartido'] = relationship('EstadosPartido', back_populates='partidos')
    local_equipo: Mapped['Equipos'] = relationship('Equipos', foreign_keys=[local_equipo_id], back_populates='partidos_local_equipo')
    torneo: Mapped['Torneos'] = relationship('Torneos', back_populates='partidos')
    visitante_equipo: Mapped['Equipos'] = relationship('Equipos', foreign_keys=[visitante_equipo_id], back_populates='partidos_visitante_equipo')
    evaluaciones_jugador: Mapped[list['EvaluacionesJugador']] = relationship('EvaluacionesJugador', back_populates='partido')
    formaciones: Mapped[list['Formaciones']] = relationship('Formaciones', back_populates='partido')
    partido_jugadores: Mapped[list['PartidoJugadores']] = relationship('PartidoJugadores', back_populates='partido')
    videos: Mapped[list['Videos']] = relationship('Videos', back_populates='partido')


class EvaluacionesJugador(Base):
    __tablename__ = 'evaluaciones_jugador'
    __table_args__ = (
        CheckConstraint('valor >= 1 AND valor <= 10', name='chk_valor_evaluacion'),
        ForeignKeyConstraint(['criterio_id'], ['criterios_evaluacion.id'], name='fk_eval_criterio'),
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_eval_jugador'),
        ForeignKeyConstraint(['partido_id'], ['partidos.id'], name='fk_eval_partido'),
        ForeignKeyConstraint(['scout_id'], ['scouts.id'], name='fk_eval_scout'),
        PrimaryKeyConstraint('id', name='evaluaciones_jugador_pkey'),
        Index('idx_eval_jugador', 'jugador_id'),
        Index('idx_eval_partido', 'partido_id'),
        Index('idx_evaluacion_criterio', 'criterio_id'),
        Index('idx_evaluacion_jugador', 'jugador_id'),
        Index('idx_evaluacion_partido', 'partido_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    jugador_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    criterio_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    valor: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    partido_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    scout_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    comentario: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    criterio: Mapped['CriteriosEvaluacion'] = relationship('CriteriosEvaluacion', back_populates='evaluaciones_jugador')
    jugador: Mapped['Jugadores'] = relationship('Jugadores', back_populates='evaluaciones_jugador')
    partido: Mapped[Optional['Partidos']] = relationship('Partidos', back_populates='evaluaciones_jugador')
    scout: Mapped[Optional['Scouts']] = relationship('Scouts', back_populates='evaluaciones_jugador')


class Formaciones(Base):
    __tablename__ = 'formaciones'
    __table_args__ = (
        ForeignKeyConstraint(['equipo_id'], ['equipos.id'], name='fk_formacion_equipo'),
        ForeignKeyConstraint(['partido_id'], ['partidos.id'], name='fk_formacion_partido'),
        PrimaryKeyConstraint('id', name='formaciones_pkey'),
        Index('idx_formacion_equipo', 'equipo_id'),
        Index('idx_formacion_partido', 'partido_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    partido_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    equipo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    esquema: Mapped[Optional[str]] = mapped_column(String(30))
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    equipo: Mapped['Equipos'] = relationship('Equipos', back_populates='formaciones')
    partido: Mapped['Partidos'] = relationship('Partidos', back_populates='formaciones')
    formacion_jugadores: Mapped[list['FormacionJugadores']] = relationship('FormacionJugadores', back_populates='formacion')


class PartidoJugadores(Base):
    __tablename__ = 'partido_jugadores'
    __table_args__ = (
        ForeignKeyConstraint(['equipo_id'], ['equipos.id'], name='fk_pj_equipo'),
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_pj_jugador'),
        ForeignKeyConstraint(['partido_id'], ['partidos.id'], name='fk_pj_partido'),
        ForeignKeyConstraint(['posicion_id'], ['posiciones.id'], name='fk_pj_posicion'),
        PrimaryKeyConstraint('id', name='partido_jugadores_pkey'),
        Index('idx_partido_jugador_equipo', 'equipo_id'),
        Index('idx_partido_jugador_jugador', 'jugador_id'),
        Index('idx_partido_jugador_partido', 'partido_id'),
        Index('idx_pj_jugador', 'jugador_id'),
        Index('idx_pj_partido', 'partido_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    partido_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    jugador_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    equipo_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    numero_camiseta: Mapped[Optional[int]] = mapped_column(SmallInteger)
    titular: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    capitan: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    posicion_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    minuto_entrada: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    minuto_salida: Mapped[Optional[int]] = mapped_column(SmallInteger)
    minutos_jugados: Mapped[Optional[int]] = mapped_column(SmallInteger)
    observacion: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    equipo: Mapped['Equipos'] = relationship('Equipos', back_populates='partido_jugadores')
    jugador: Mapped['Jugadores'] = relationship('Jugadores', back_populates='partido_jugadores')
    partido: Mapped['Partidos'] = relationship('Partidos', back_populates='partido_jugadores')
    posicion: Mapped[Optional['Posiciones']] = relationship('Posiciones', back_populates='partido_jugadores')


class Videos(Base):
    __tablename__ = 'videos'
    __table_args__ = (
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_video_jugador'),
        ForeignKeyConstraint(['partido_id'], ['partidos.id'], name='fk_video_partido'),
        PrimaryKeyConstraint('id', name='videos_pkey'),
        Index('idx_video_jugador', 'jugador_id'),
        Index('idx_video_partido', 'partido_id')
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    url: Mapped[str] = mapped_column(Text, nullable=False)
    jugador_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    partido_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    titulo: Mapped[Optional[str]] = mapped_column(String(200))
    tipo: Mapped[Optional[str]] = mapped_column(String(50))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    fecha: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    jugador: Mapped[Optional['Jugadores']] = relationship('Jugadores', back_populates='videos')
    partido: Mapped[Optional['Partidos']] = relationship('Partidos', back_populates='videos')


class FormacionJugadores(Base):
    __tablename__ = 'formacion_jugadores'
    __table_args__ = (
        ForeignKeyConstraint(['formacion_id'], ['formaciones.id'], name='fk_fj_formacion'),
        ForeignKeyConstraint(['jugador_id'], ['jugadores.id'], name='fk_fj_jugador'),
        ForeignKeyConstraint(['posicion_id'], ['posiciones.id'], name='fk_fj_posicion'),
        PrimaryKeyConstraint('formacion_id', 'jugador_id', name='formacion_jugadores_pkey')
    )

    formacion_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    jugador_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    posicion_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True))
    ubicacion: Mapped[Optional[str]] = mapped_column(String(50))
    orden: Mapped[Optional[int]] = mapped_column(SmallInteger)

    formacion: Mapped['Formaciones'] = relationship('Formaciones', back_populates='formacion_jugadores')
    jugador: Mapped['Jugadores'] = relationship('Jugadores', back_populates='formacion_jugadores')
    posicion: Mapped[Optional['Posiciones']] = relationship('Posiciones', back_populates='formacion_jugadores')
