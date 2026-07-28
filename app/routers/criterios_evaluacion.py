from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.criterio_evaluacion import (
    CriterioEvaluacionCreate,
    CriterioEvaluacionResponse,
    CriterioEvaluacionUpdate,
)
from app.services.criterio_evaluacion_service import CriterioEvaluacionService

router = APIRouter(prefix="/criterios_evaluacion", tags=["Criterios de evaluación"])


@router.get("/", response_model=list[CriterioEvaluacionResponse])
def listar_criterios_evaluacion(db: Session = Depends(get_db)):
    return CriterioEvaluacionService(db).get_all()


@router.get("/{criterio_id}", response_model=CriterioEvaluacionResponse)
def obtener_criterio_evaluacion(criterio_id: UUID, db: Session = Depends(get_db)):
    return CriterioEvaluacionService(db).get(criterio_id)


@router.post("/", response_model=CriterioEvaluacionResponse, status_code=status.HTTP_201_CREATED)
def crear_criterio_evaluacion(payload: CriterioEvaluacionCreate, db: Session = Depends(get_db)):
    return CriterioEvaluacionService(db).create(payload)


@router.put("/{criterio_id}", response_model=CriterioEvaluacionResponse)
def actualizar_criterio_evaluacion(criterio_id: UUID, payload: CriterioEvaluacionUpdate, db: Session = Depends(get_db)):
    return CriterioEvaluacionService(db).update(criterio_id, payload)


@router.delete("/{criterio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_criterio_evaluacion(criterio_id: UUID, db: Session = Depends(get_db)):
    CriterioEvaluacionService(db).delete(criterio_id)
    return None
