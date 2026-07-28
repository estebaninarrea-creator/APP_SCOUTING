import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.archivo_adjunto import ArchivosAdjuntos
from app.models.evaluacion_jugador import EvaluacionesJugador
from app.models.informe_scouting import InformesScouting
from app.models.video import Videos
from app.schemas.scouting import (
    ArchivoAdjuntoCreate,
    ArchivoAdjuntoUpdate,
    EvaluacionJugadorCreate,
    EvaluacionJugadorUpdate,
    InformeScoutingCreate,
    InformeScoutingUpdate,
    VideoCreate,
    VideoUpdate,
)

logger = logging.getLogger(__name__)


def get_informes_scouting(db: Session):
    logger.info("Obteniendo todos los informes de scouting")
    try:
        return db.query(InformesScouting).order_by(InformesScouting.created_at.desc()).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener informes: {str(e)}")
        raise


def get_informe_scouting(db: Session, informe_id: UUID):
    logger.info(f"Obteniendo informe {informe_id}")
    try:
        return db.query(InformesScouting).filter(InformesScouting.id == informe_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener informe {informe_id}: {str(e)}")
        raise


def create_informe_scouting(db: Session, informe: InformeScoutingCreate):
    logger.info("Creando nuevo informe de scouting")
    try:
        nuevo = InformesScouting(**informe.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Informe creado: {nuevo.id}")
        return nuevo
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear informe: {str(e)}")
        raise


def update_informe_scouting(db: Session, informe_id: UUID, informe: InformeScoutingUpdate):
    logger.info(f"Actualizando informe {informe_id}")
    try:
        existing = get_informe_scouting(db, informe_id)
        if not existing:
            logger.warning(f"Informe no encontrado: {informe_id}")
            return None
        for key, value in informe.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Informe actualizado: {informe_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar informe {informe_id}: {str(e)}")
        raise


def delete_informe_scouting(db: Session, informe_id: UUID):
    logger.info(f"Eliminando informe {informe_id}")
    try:
        existing = get_informe_scouting(db, informe_id)
        if existing:
            db.delete(existing)
            db.commit()
            logger.info(f"Informe eliminado: {informe_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar informe {informe_id}: {str(e)}")
        raise


def get_evaluaciones_jugador(db: Session):
    logger.info("Obteniendo todas las evaluaciones")
    try:
        return db.query(EvaluacionesJugador).order_by(EvaluacionesJugador.created_at.desc()).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener evaluaciones: {str(e)}")
        raise


def get_evaluacion_jugador(db: Session, evaluacion_id: UUID):
    logger.info(f"Obteniendo evaluación {evaluacion_id}")
    try:
        return db.query(EvaluacionesJugador).filter(EvaluacionesJugador.id == evaluacion_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener evaluación {evaluacion_id}: {str(e)}")
        raise


def create_evaluacion_jugador(db: Session, evaluacion: EvaluacionJugadorCreate):
    logger.info("Creando nueva evaluación")
    try:
        nuevo = EvaluacionesJugador(**evaluacion.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Evaluación creada: {nuevo.id}")
        return nuevo
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear evaluación: {str(e)}")
        raise


def update_evaluacion_jugador(db: Session, evaluacion_id: UUID, evaluacion: EvaluacionJugadorUpdate):
    logger.info(f"Actualizando evaluación {evaluacion_id}")
    try:
        existing = get_evaluacion_jugador(db, evaluacion_id)
        if not existing:
            logger.warning(f"Evaluación no encontrada: {evaluacion_id}")
            return None
        for key, value in evaluacion.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        logger.info(f"Evaluación actualizada: {evaluacion_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar evaluación {evaluacion_id}: {str(e)}")
        raise


def delete_evaluacion_jugador(db: Session, evaluacion_id: UUID):
    logger.info(f"Eliminando evaluación {evaluacion_id}")
    try:
        existing = get_evaluacion_jugador(db, evaluacion_id)
        if existing:
            db.delete(existing)
            db.commit()
            logger.info(f"Evaluación eliminada: {evaluacion_id}")
        return existing
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar evaluación {evaluacion_id}: {str(e)}")
        raise


def get_videos(db: Session):
    return db.query(Videos).order_by(Videos.fecha_carga.desc()).all()


def get_video(db: Session, video_id: UUID):
    return db.query(Videos).filter(Videos.id == video_id).first()


def create_video(db: Session, video: VideoCreate):
    nuevo = Videos(**video.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_video(db: Session, video_id: UUID, video: VideoUpdate):
    existing = get_video(db, video_id)
    if not existing:
        return None
    for key, value in video.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing


def delete_video(db: Session, video_id: UUID):
    existing = get_video(db, video_id)
    if existing:
        db.delete(existing)
        db.commit()
    return existing


def get_archivos_adjuntos(db: Session):
    return db.query(ArchivosAdjuntos).order_by(ArchivosAdjuntos.fecha_carga.desc()).all()


def get_archivo_adjunto(db: Session, archivo_id: UUID):
    return db.query(ArchivosAdjuntos).filter(ArchivosAdjuntos.id == archivo_id).first()


def create_archivo_adjunto(db: Session, archivo: ArchivoAdjuntoCreate):
    nuevo = ArchivosAdjuntos(**archivo.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_archivo_adjunto(db: Session, archivo_id: UUID, archivo: ArchivoAdjuntoUpdate):
    existing = get_archivo_adjunto(db, archivo_id)
    if not existing:
        return None
    for key, value in archivo.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing


def delete_archivo_adjunto(db: Session, archivo_id: UUID):
    existing = get_archivo_adjunto(db, archivo_id)
    if existing:
        db.delete(existing)
        db.commit()
    return existing
