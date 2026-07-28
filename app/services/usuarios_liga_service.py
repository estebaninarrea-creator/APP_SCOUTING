from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.usuarios_ligas import UsuariosLigas


class UsuariosLigaService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.query(UsuariosLigas).all()

    def get(self, usuario_id: UUID, liga_id: UUID):
        item = self.db.query(UsuariosLigas).filter(
            UsuariosLigas.usuario_id == usuario_id,
            UsuariosLigas.liga_id == liga_id,
        ).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación usuario-liga no encontrada")
        return item

    def create(self, payload):
        try:
            item = UsuariosLigas(**payload.model_dump())
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Relación inválida o duplicada")
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear relación usuario-liga")

    def delete(self, usuario_id: UUID, liga_id: UUID):
        try:
            item = self.get(usuario_id, liga_id)
            self.db.delete(item)
            self.db.commit()
        except HTTPException:
            raise
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar relación usuario-liga")
