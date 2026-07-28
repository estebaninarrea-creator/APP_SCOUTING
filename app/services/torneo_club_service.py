from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.torneo_club import TorneosClubes


class TorneoClubService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.query(TorneosClubes).all()

    def get(self, torneo_id: UUID, equipo_id: UUID):
        item = self.db.query(TorneosClubes).filter(
            TorneosClubes.torneo_id == torneo_id,
            TorneosClubes.equipo_id == equipo_id,
        ).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación torneo-equipo no encontrada")
        return item

    def create(self, payload):
        try:
            item = TorneosClubes(**payload.model_dump())
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Relación inválida o duplicada")
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear relación torneo-equipo")

    def update(self, torneo_id: UUID, equipo_id: UUID, payload):
        try:
            item = self.get(torneo_id, equipo_id)
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            return item
        except HTTPException:
            raise
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar relación torneo-equipo")

    def delete(self, torneo_id: UUID, equipo_id: UUID):
        try:
            item = self.get(torneo_id, equipo_id)
            self.db.delete(item)
            self.db.commit()
        except HTTPException:
            raise
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar relación torneo-equipo")
