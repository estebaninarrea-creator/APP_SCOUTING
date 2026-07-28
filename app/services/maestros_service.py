import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.categoria import Categorias
from app.models.ciudad import Ciudades
from app.models.club import Clubes
from app.models.estadio import Estadios
from app.models.jugador import Jugadores
from app.models.liga import Ligas
from app.models.pais import Paises
from app.models.posicion import Posiciones
from app.models.provincia import Provincias
from app.models.temporada import Temporadas
from app.models.tipo_torneo import TiposTorneo

logger = logging.getLogger(__name__)


def _normalize_text(value) -> str:
    return (value or "").strip()


def _ensure_default_pais(db: Session):
    existing = db.query(Paises).order_by(Paises.nombre).first()
    if existing:
        return existing.id

    default_pais = Paises(
        nombre="Argentina",
        codigo_iso2="AR",
        codigo_iso3="ARG",
        codigo_fifa="ARG",
    )
    db.add(default_pais)
    db.commit()
    db.refresh(default_pais)
    return default_pais.id


def _get_default_pais_id(db: Session):
    pais = db.query(Paises).order_by(Paises.nombre).first()
    return pais.id if pais else _ensure_default_pais(db)


def get_datos_maestros(db: Session):
    logger.info("Obteniendo datos maestros")
    try:
        provincias = db.query(Provincias).order_by(Provincias.nombre).all()
        ciudades = db.query(Ciudades).order_by(Ciudades.nombre).all()
        posiciones = db.query(Posiciones).all()
        temporadas = db.query(Temporadas).order_by(Temporadas.nombre).all()
        categorias = db.query(Categorias).order_by(Categorias.nombre).all()
        tipos_torneo = db.query(TiposTorneo).order_by(TiposTorneo.nombre).all()

        def sort_key(item):
            nombre = (getattr(item, "nombre", "") or "").lower()
            codigo = (getattr(item, "codigo", "") or "").lower()
            return (nombre, codigo)

        posiciones = sorted(posiciones, key=sort_key)

        logger.info(f"Datos maestros obtenidos: provincias={len(provincias)}, ciudades={len(ciudades)}, posiciones={len(posiciones)}")
        return {
            "provincias": provincias,
            "ciudades": ciudades,
            "posiciones": posiciones,
            "temporadas": temporadas,
            "categorias": categorias,
            "tipos_torneo": tipos_torneo,
        }
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener datos maestros: {str(e)}")
        raise


def get_paises(db: Session):
    logger.info("Obteniendo países")
    try:
        return db.query(Paises).order_by(Paises.nombre).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener países: {str(e)}")
        raise


def get_pais(db: Session, pais_id):
    logger.info(f"Obteniendo país {pais_id}")
    try:
        return db.query(Paises).filter(Paises.id == pais_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener país {pais_id}: {str(e)}")
        raise


def create_pais(db: Session, pais):
    logger.info("Creando nuevo país")
    try:
        nuevo = Paises(**pais.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"País creado: {nuevo.id}")
        return nuevo
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear país: {str(e)}")
        raise


def update_pais(db: Session, pais_id, pais):
    logger.info(f"Actualizando país {pais_id}")
    try:
        existing = get_pais(db, pais_id)
        if not existing:
            logger.warning(f"País no encontrado: {pais_id}")
            return None
        for key, value in pais.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"País actualizado: {pais_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar país {pais_id}: {str(e)}")
        raise


def delete_pais(db: Session, pais_id):
    logger.info(f"Eliminando país {pais_id}")
    try:
        existing = get_pais(db, pais_id)
        if existing:
            db.delete(existing)
            db.commit()
            logger.info(f"País eliminado: {pais_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar país {pais_id}: {str(e)}")
        raise


def get_provincias(db: Session):
    logger.info("Obteniendo provincias")
    try:
        return db.query(Provincias).order_by(Provincias.nombre).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener provincias: {str(e)}")
        raise


def get_provincia(db: Session, provincia_id):
    logger.info(f"Obteniendo provincia {provincia_id}")
    try:
        return db.query(Provincias).filter(Provincias.id == provincia_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener provincia {provincia_id}: {str(e)}")
        raise


def create_provincia(db: Session, provincia):
    logger.info("Creando nueva provincia")
    try:
        payload = provincia.model_dump()
        payload["nombre"] = _normalize_text(payload.get("nombre"))
        if not payload["nombre"]:
            logger.warning("Nombre de provincia vacío")
            raise ValueError("El nombre de la provincia es obligatorio")

        if not payload.get("pais_id"):
            payload["pais_id"] = _get_default_pais_id(db)

        existing = db.query(Provincias).filter(Provincias.nombre.ilike(payload["nombre"])).first()
        if existing:
            logger.info(f"Provincia existente: {existing.id}")
            return existing

        nuevo = Provincias(**payload)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Provincia creada: {nuevo.id}")
        return nuevo
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear provincia: {str(e)}")
        raise


def create_provincias_bulk(db: Session, provincias=None):
    default_provincias = [
        "Buenos Aires",
        "Catamarca",
        "Chaco",
        "Chubut",
        "Córdoba",
        "Corrientes",
        "Entre Ríos",
        "Formosa",
        "Jujuy",
        "La Pampa",
        "La Rioja",
        "Mendoza",
        "Misiones",
        "Neuquén",
        "Río Negro",
        "Salta",
        "San Juan",
        "San Luis",
        "Santa Cruz",
        "Santa Fe",
        "Santiago del Estero",
        "Tierra del Fuego",
        "Tucumán",
    ]

    payloads = []
    if provincias is None:
        pais_id = _get_default_pais_id(db)
        payloads = [{"nombre": nombre, "pais_id": pais_id} for nombre in default_provincias]
    else:
        payloads = [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in provincias]

    created = []
    for payload in payloads:
        nombre = _normalize_text(payload.get("nombre"))
        if not nombre:
            continue
        pais_id = payload.get("pais_id") or _get_default_pais_id(db)
        if not pais_id:
            continue

        existing = db.query(Provincias).filter(Provincias.nombre.ilike(nombre)).first()
        if existing:
            created.append(existing)
            continue

        nuevo = Provincias(nombre=nombre, pais_id=pais_id)
        db.add(nuevo)
        created.append(nuevo)

    db.commit()
    for item in created:
        db.refresh(item)
    return created


def update_provincia(db: Session, provincia_id, provincia):
    existing = get_provincia(db, provincia_id)
    if not existing:
        return None
    for key, value in provincia.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing


def delete_provincia(db: Session, provincia_id):
    existing = get_provincia(db, provincia_id)
    if not existing:
        return None

    related_cities = db.query(Ciudades).filter(Ciudades.provincia_id == provincia_id).all()
    related_leagues = db.query(Ligas).filter(Ligas.provincia_id == provincia_id).all()

    if related_cities or related_leagues:
        raise ValueError("No se puede eliminar la provincia porque tiene ciudades o ligas relacionadas")

    db.delete(existing)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return existing


def get_ciudades(db: Session):
    return db.query(Ciudades).order_by(Ciudades.nombre).all()


def get_ciudad(db: Session, ciudad_id):
    return db.query(Ciudades).filter(Ciudades.id == ciudad_id).first()


def create_ciudad(db: Session, ciudad):
    payload = ciudad.model_dump()
    payload["nombre"] = _normalize_text(payload.get("nombre"))
    if not payload["nombre"]:
        raise ValueError("El nombre de la ciudad es obligatorio")
    if not payload.get("provincia_id"):
        default_provincia = db.query(Provincias).order_by(Provincias.nombre).first()
        if default_provincia:
            payload["provincia_id"] = default_provincia.id
    nuevo = Ciudades(**payload)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_ciudad(db: Session, ciudad_id, ciudad):
    existing = get_ciudad(db, ciudad_id)
    if not existing:
        return None
    for key, value in ciudad.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing


def delete_ciudad(db: Session, ciudad_id):
    existing = get_ciudad(db, ciudad_id)
    if not existing:
        return None

    related_clubs = db.query(Clubes).filter(Clubes.ciudad_id == ciudad_id).all()
    related_estadios = db.query(Estadios).filter(Estadios.ciudad_id == ciudad_id).all()
    related_jugadores = db.query(Jugadores).filter(Jugadores.ciudad_id == ciudad_id).all()

    if related_clubs or related_estadios or related_jugadores:
        raise ValueError("No se puede eliminar la ciudad porque tiene clubes, estadios o jugadores relacionados")

    db.delete(existing)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return existing


def get_posiciones(db: Session):
    return db.query(Posiciones).order_by(Posiciones.nombre).all()


def get_posicion(db: Session, posicion_id):
    return db.query(Posiciones).filter(Posiciones.id == posicion_id).first()


def create_posicion(db: Session, posicion):
    payload = posicion.model_dump()
    payload["codigo"] = _normalize_text(payload.get("codigo")).upper()
    payload["nombre"] = _normalize_text(payload.get("nombre"))
    if payload.get("orden") is None:
        payload["orden"] = 1
    if not payload["codigo"] or not payload["nombre"]:
        raise ValueError("Código y nombre de la posición son obligatorios")

    existing = db.query(Posiciones).filter(Posiciones.codigo == payload["codigo"]).first()
    if existing:
        return existing

    nuevo = Posiciones(**payload)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_posicion(db: Session, posicion_id, posicion):
    existing = get_posicion(db, posicion_id)
    if not existing:
        return None
    for key, value in posicion.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing


def delete_posicion(db: Session, posicion_id):
    existing = get_posicion(db, posicion_id)
    if existing:
        db.delete(existing)
        db.commit()
    return existing
