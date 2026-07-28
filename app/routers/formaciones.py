from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.formacion import FormacionCreate, FormacionResponse, FormacionUpdate
from app.services.formacion_service import (
    create_formacion,
    delete_formacion,
    get_formacion,
    get_formaciones,
    update_formacion,
)

router = APIRouter(prefix="/formaciones", tags=["Formaciones"])


@router.get("/", response_model=list[FormacionResponse])
def listar_formaciones(db: Session = Depends(get_db)):
    """Lista todas las formaciones"""
    return get_formaciones(db)


@router.get("/{formacion_id}", response_model=FormacionResponse)
def obtener_formacion(formacion_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una formación por ID"""
    return get_formacion(db, formacion_id)


@router.post("/", response_model=FormacionResponse, status_code=status.HTTP_201_CREATED)
def crear_formacion(formacion: FormacionCreate, db: Session = Depends(get_db)):
    """Crea una nueva formación"""
    return create_formacion(db, formacion)


@router.put("/{formacion_id}", response_model=FormacionResponse)
def actualizar_formacion(formacion_id: UUID, formacion: FormacionUpdate, db: Session = Depends(get_db)):
    """Actualiza una formación existente"""
    return update_formacion(db, formacion_id, formacion)


@router.delete("/{formacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_formacion(formacion_id: UUID, db: Session = Depends(get_db)):
    """Elimina una formación"""
    delete_formacion(db, formacion_id)
    return None
