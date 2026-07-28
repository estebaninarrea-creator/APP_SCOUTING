from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_permissions
from app.schemas.partido import PartidoCreate, PartidoResponse, PartidoUpdate
from app.services.partido_service import (
    create_partido,
    delete_partido,
    get_partido,
    get_partidos,
    update_partido,
)

router = APIRouter(prefix="/partidos", tags=["Partidos"])


@router.get("/", response_model=list[PartidoResponse])
def listar_partidos(db: Session = Depends(get_db)):
    partidos = get_partidos(db)
    result = []
    for partido in partidos:
        result.append(
            {
                "id": partido.id,
                "torneo_id": partido.torneo_id,
                "equipo_local_id": getattr(partido, "equipo_local_id", None),
                "equipo_visitante_id": getattr(partido, "equipo_visitante_id", None),
                "local_equipo_id": getattr(partido, "equipo_local_id", None),
                "visitante_equipo_id": getattr(partido, "equipo_visitante_id", None),
                "estado_id": partido.estado_id,
                "comet_id": partido.comet_id,
                "fecha_partido": partido.fecha_partido,
                "hora": partido.hora,
                "cancha_id": partido.cancha_id,
                "arbitro_id": partido.arbitro_id,
                "goles_local": partido.goles_local,
                "goles_visitante": partido.goles_visitante,
                "observaciones": partido.observaciones,
                "created_at": partido.created_at,
                "updated_at": partido.updated_at,
            }
        )
    return result


@router.get("/{partido_id}", response_model=PartidoResponse)
def obtener_partido(partido_id: UUID, db: Session = Depends(get_db)):
    partido = get_partido(db, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido


@router.post("/", response_model=PartidoResponse)
def crear_partido(partido: PartidoCreate, db: Session = Depends(get_db), _user=Depends(require_permissions("partidos:manage"))):
    return create_partido(db, partido)


@router.put("/{partido_id}", response_model=PartidoResponse)
def actualizar_partido(partido_id: UUID, partido: PartidoUpdate, db: Session = Depends(get_db), _user=Depends(require_permissions("partidos:manage"))):
    updated = update_partido(db, partido_id, partido)
    if not updated:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return updated


@router.delete("/{partido_id}")
def eliminar_partido(partido_id: UUID, db: Session = Depends(get_db), _user=Depends(require_permissions("partidos:manage"))):
    deleted = delete_partido(db, partido_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return {"mensaje": "Partido eliminado"}
