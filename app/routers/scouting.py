from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.scouting import (
    ArchivoAdjuntoCreate,
    ArchivoAdjuntoResponse,
    ArchivoAdjuntoUpdate,
    EvaluacionJugadorCreate,
    EvaluacionJugadorResponse,
    EvaluacionJugadorUpdate,
    InformeScoutingCreate,
    InformeScoutingResponse,
    InformeScoutingUpdate,
    VideoCreate,
    VideoResponse,
    VideoUpdate,
)
from app.services.scouting_service import (
    create_archivo_adjunto,
    create_evaluacion_jugador,
    create_informe_scouting,
    create_video,
    delete_archivo_adjunto,
    delete_evaluacion_jugador,
    delete_informe_scouting,
    delete_video,
    get_archivo_adjunto,
    get_archivos_adjuntos,
    get_evaluacion_jugador,
    get_evaluaciones_jugador,
    get_informe_scouting,
    get_informes_scouting,
    get_video,
    get_videos,
    update_archivo_adjunto,
    update_evaluacion_jugador,
    update_informe_scouting,
    update_video,
)

router = APIRouter(prefix="/scouting", tags=["Scouting"])


@router.get("/informes", response_model=list[InformeScoutingResponse])
def listar_informes_scouting(db: Session = Depends(get_db)):
    return get_informes_scouting(db)


@router.post("/informes", response_model=InformeScoutingResponse)
def crear_informe_scouting(informe: InformeScoutingCreate, db: Session = Depends(get_db)):
    return create_informe_scouting(db, informe)


@router.get("/informes/{informe_id}", response_model=InformeScoutingResponse)
def obtener_informe_scouting(informe_id: UUID, db: Session = Depends(get_db)):
    informe = get_informe_scouting(db, informe_id)
    if not informe:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return informe


@router.put("/informes/{informe_id}", response_model=InformeScoutingResponse)
def actualizar_informe_scouting(informe_id: UUID, informe: InformeScoutingUpdate, db: Session = Depends(get_db)):
    updated = update_informe_scouting(db, informe_id, informe)
    if not updated:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return updated


@router.delete("/informes/{informe_id}")
def eliminar_informe_scouting(informe_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_informe_scouting(db, informe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return {"mensaje": "Informe eliminado"}


@router.get("/evaluaciones", response_model=list[EvaluacionJugadorResponse])
def listar_evaluaciones_jugador(db: Session = Depends(get_db)):
    return get_evaluaciones_jugador(db)


@router.post("/evaluaciones", response_model=EvaluacionJugadorResponse)
def crear_evaluacion_jugador(evaluacion: EvaluacionJugadorCreate, db: Session = Depends(get_db)):
    return create_evaluacion_jugador(db, evaluacion)


@router.get("/evaluaciones/{evaluacion_id}", response_model=EvaluacionJugadorResponse)
def obtener_evaluacion_jugador(evaluacion_id: UUID, db: Session = Depends(get_db)):
    evaluacion = get_evaluacion_jugador(db, evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluacion


@router.put("/evaluaciones/{evaluacion_id}", response_model=EvaluacionJugadorResponse)
def actualizar_evaluacion_jugador(evaluacion_id: UUID, evaluacion: EvaluacionJugadorUpdate, db: Session = Depends(get_db)):
    updated = update_evaluacion_jugador(db, evaluacion_id, evaluacion)
    if not updated:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return updated


@router.delete("/evaluaciones/{evaluacion_id}")
def eliminar_evaluacion_jugador(evaluacion_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_evaluacion_jugador(db, evaluacion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return {"mensaje": "Evaluación eliminada"}


@router.get("/videos", response_model=list[VideoResponse])
def listar_videos(db: Session = Depends(get_db)):
    return get_videos(db)


@router.post("/videos", response_model=VideoResponse)
def crear_video(video: VideoCreate, db: Session = Depends(get_db)):
    return create_video(db, video)


@router.get("/videos/{video_id}", response_model=VideoResponse)
def obtener_video(video_id: UUID, db: Session = Depends(get_db)):
    video = get_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return video


@router.put("/videos/{video_id}", response_model=VideoResponse)
def actualizar_video(video_id: UUID, video: VideoUpdate, db: Session = Depends(get_db)):
    updated = update_video(db, video_id, video)
    if not updated:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return updated


@router.delete("/videos/{video_id}")
def eliminar_video(video_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_video(db, video_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return {"mensaje": "Video eliminado"}


@router.get("/archivos", response_model=list[ArchivoAdjuntoResponse])
def listar_archivos_adjuntos(db: Session = Depends(get_db)):
    return get_archivos_adjuntos(db)


@router.post("/archivos", response_model=ArchivoAdjuntoResponse)
def crear_archivo_adjunto(archivo: ArchivoAdjuntoCreate, db: Session = Depends(get_db)):
    return create_archivo_adjunto(db, archivo)


@router.get("/archivos/{archivo_id}", response_model=ArchivoAdjuntoResponse)
def obtener_archivo_adjunto(archivo_id: UUID, db: Session = Depends(get_db)):
    archivo = get_archivo_adjunto(db, archivo_id)
    if not archivo:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return archivo


@router.put("/archivos/{archivo_id}", response_model=ArchivoAdjuntoResponse)
def actualizar_archivo_adjunto(archivo_id: UUID, archivo: ArchivoAdjuntoUpdate, db: Session = Depends(get_db)):
    updated = update_archivo_adjunto(db, archivo_id, archivo)
    if not updated:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return updated


@router.delete("/archivos/{archivo_id}")
def eliminar_archivo_adjunto(archivo_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_archivo_adjunto(db, archivo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return {"mensaje": "Archivo eliminado"}
