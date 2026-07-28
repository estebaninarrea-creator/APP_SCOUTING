from fastapi import HTTPException, status

from app.models.cancha import Canchas
from app.services.crud_service import CRUDService


class CanchaService(CRUDService):
    def __init__(self, db):
        super().__init__(db, Canchas)

    def _ensure_single_cancha_per_estadio(self, estadio_id, exclude_id=None):
        query = self.db.query(Canchas).filter(Canchas.estadio_id == estadio_id)
        if exclude_id is not None:
            query = query.filter(Canchas.id != exclude_id)
        if query.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cancha para este estadio. Use editar para actualizar superficie e iluminación.",
            )

    def create(self, data):
        self._ensure_single_cancha_per_estadio(data.estadio_id)
        return super().create(data)

    def update(self, item_id, data):
        existing = self.get(item_id)
        estadio_id = data.estadio_id if data.estadio_id is not None else existing.estadio_id
        self._ensure_single_cancha_per_estadio(estadio_id, exclude_id=existing.id)
        return super().update(item_id, data)
