import logging
from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.models.equipo import Equipos
from app.models.plantel import Planteles
from app.schemas.plantel import PlantelCreate, PlantelUpdate

logger = logging.getLogger(__name__)


def _is_overlap(
    desde_a: date,
    hasta_a: date | None,
    desde_b: date,
    hasta_b: date | None,
) -> bool:
    """Determina si dos rangos de fechas se superponen (fecha_hasta None = abierto)."""
    fin_a = hasta_a or date.max
    fin_b = hasta_b or date.max
    return desde_a <= fin_b and desde_b <= fin_a


def _validate_jugador_unico_por_temporada(
    db: Session,
    jugador_id: UUID,
    equipo_id: UUID,
    fecha_desde: date,
    fecha_hasta: date | None,
    exclude_plantel_id: UUID | None = None,
) -> None:
    if fecha_hasta and fecha_hasta < fecha_desde:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha_hasta no puede ser anterior a la fecha_desde",
        )

    equipo = db.query(Equipos).filter(Equipos.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=400, detail="Error: equipo no existe")

    conflict_query = (
        db.query(Planteles)
        .join(Equipos, Equipos.id == Planteles.equipo_id)
        .filter(
            Planteles.jugador_id == jugador_id,
            Equipos.temporada_id == equipo.temporada_id,
            Planteles.equipo_id != equipo_id,
        )
    )

    if exclude_plantel_id:
        conflict_query = conflict_query.filter(Planteles.id != exclude_plantel_id)

    conflict = conflict_query.first()
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El jugador ya está asignado a otro equipo en la misma temporada",
        )

    same_team_query = (
        db.query(Planteles)
        .filter(
            Planteles.jugador_id == jugador_id,
            Planteles.equipo_id == equipo_id,
        )
    )

    if exclude_plantel_id:
        same_team_query = same_team_query.filter(Planteles.id != exclude_plantel_id)

    for existing in same_team_query.all():
        if _is_overlap(
            fecha_desde,
            fecha_hasta,
            existing.fecha_desde,
            existing.fecha_hasta,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El jugador ya tiene un período de plantel superpuesto en este equipo",
            )


def get_planteles(
    db: Session,
    equipo_id: UUID | None = None,
    temporada_id: UUID | None = None,
) -> list[Planteles]:
    """Obtiene planteles, opcionalmente filtrados por equipo y/o temporada"""
    logger.info("Obteniendo todos los planteles")
    try:
        query = (
            db.query(Planteles)
            .options(joinedload(Planteles.equipo))
            .join(Equipos, Equipos.id == Planteles.equipo_id)
        )

        if equipo_id:
            query = query.filter(Planteles.equipo_id == equipo_id)

        if temporada_id:
            query = query.filter(Equipos.temporada_id == temporada_id)

        return query.order_by(Planteles.created_at.desc()).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener planteles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener planteles")


def get_plantel(db: Session, plantel_id: UUID) -> Planteles:
    """Obtiene un plantel por ID"""
    logger.info(f"Obteniendo plantel {plantel_id}")
    try:
        plantel = db.query(Planteles).filter(Planteles.id == plantel_id).first()
        if not plantel:
            logger.warning(f"Plantel {plantel_id} no encontrado")
            raise HTTPException(status_code=404, detail="Plantel no encontrado")
        return plantel
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener plantel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener plantel")


def create_plantel(db: Session, plantel: PlantelCreate) -> Planteles:
    """Crea un nuevo plantel"""
    logger.info(f"Creando plantel para equipo {plantel.equipo_id}, jugador {plantel.jugador_id}")
    try:
        _validate_jugador_unico_por_temporada(
            db=db,
            jugador_id=plantel.jugador_id,
            equipo_id=plantel.equipo_id,
            fecha_desde=plantel.fecha_desde,
            fecha_hasta=plantel.fecha_hasta,
        )

        db_plantel = Planteles(**plantel.model_dump())
        db.add(db_plantel)
        db.commit()
        db.refresh(db_plantel)
        logger.info(f"Plantel creado: {db_plantel.id}")
        return db_plantel
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: equipo o jugador no existen")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear plantel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear plantel")


def update_plantel(db: Session, plantel_id: UUID, plantel: PlantelUpdate) -> Planteles:
    """Actualiza un plantel existente"""
    logger.info(f"Actualizando plantel {plantel_id}")
    try:
        db_plantel = db.query(Planteles).filter(Planteles.id == plantel_id).first()
        if not db_plantel:
            logger.warning(f"Plantel {plantel_id} no encontrado")
            raise HTTPException(status_code=404, detail="Plantel no encontrado")

        update_data = plantel.model_dump(exclude_unset=True)

        equipo_id_final = update_data.get("equipo_id", db_plantel.equipo_id)
        jugador_id_final = update_data.get("jugador_id", db_plantel.jugador_id)
        fecha_desde_final = update_data.get("fecha_desde", db_plantel.fecha_desde)
        fecha_hasta_final = update_data.get("fecha_hasta", db_plantel.fecha_hasta)

        _validate_jugador_unico_por_temporada(
            db=db,
            jugador_id=jugador_id_final,
            equipo_id=equipo_id_final,
            fecha_desde=fecha_desde_final,
            fecha_hasta=fecha_hasta_final,
            exclude_plantel_id=plantel_id,
        )

        for key, value in update_data.items():
            setattr(db_plantel, key, value)
        
        db.commit()
        db.refresh(db_plantel)
        logger.info(f"Plantel actualizado: {db_plantel.id}")
        return db_plantel
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: equipo o jugador no existen")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar plantel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar plantel")


def delete_plantel(db: Session, plantel_id: UUID) -> None:
    """Elimina un plantel"""
    logger.info(f"Eliminando plantel {plantel_id}")
    try:
        db_plantel = db.query(Planteles).filter(Planteles.id == plantel_id).first()
        if not db_plantel:
            logger.warning(f"Plantel {plantel_id} no encontrado")
            raise HTTPException(status_code=404, detail="Plantel no encontrado")
        
        db.delete(db_plantel)
        db.commit()
        logger.info(f"Plantel eliminado: {db_plantel.id}")
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad: {str(e)}")
        raise HTTPException(status_code=400, detail="No se puede eliminar el plantel")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar plantel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar plantel")
