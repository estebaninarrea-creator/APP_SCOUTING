from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.usuarios_liga import UsuarioLigaCreate, UsuarioLigaResponse
from app.services.usuarios_liga_service import UsuariosLigaService

router = APIRouter(prefix="/usuarios_ligas", tags=["Usuarios-Ligas"])


@router.get("/", response_model=list[UsuarioLigaResponse])
def listar_usuarios_ligas(db: Session = Depends(get_db)):
    return UsuariosLigaService(db).get_all()


@router.get("/{usuario_id}/{liga_id}", response_model=UsuarioLigaResponse)
def obtener_usuario_liga(usuario_id: UUID, liga_id: UUID, db: Session = Depends(get_db)):
    return UsuariosLigaService(db).get(usuario_id, liga_id)


@router.post("/", response_model=UsuarioLigaResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario_liga(payload: UsuarioLigaCreate, db: Session = Depends(get_db)):
    return UsuariosLigaService(db).create(payload)


@router.delete("/{usuario_id}/{liga_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario_liga(usuario_id: UUID, liga_id: UUID, db: Session = Depends(get_db)):
    UsuariosLigaService(db).delete(usuario_id, liga_id)
    return None
