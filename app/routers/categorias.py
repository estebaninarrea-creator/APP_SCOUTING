from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from app.services.categoria_service import (
    create_categoria,
    delete_categoria,
    get_categoria,
    get_categorias,
    update_categoria,
)

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    """Lista todas las categorías"""
    return get_categorias(db)


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una categoría por ID"""
    return get_categoria(db, categoria_id)


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una nueva categoría"""
    return create_categoria(db, categoria)


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(categoria_id: UUID, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    """Actualiza una categoría existente"""
    return update_categoria(db, categoria_id, categoria)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    """Elimina una categoría"""
    delete_categoria(db, categoria_id)
    return None
