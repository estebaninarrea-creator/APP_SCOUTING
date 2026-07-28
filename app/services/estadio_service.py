from fastapi import HTTPException, status

from app.models.cancha import Canchas
from app.models.estadio import Estadios
from app.services.crud_service import CRUDService


class EstadioService(CRUDService):
    def __init__(self, db):
        super().__init__(db, Estadios)

    def _validate_cancha(self, cancha_id):
        if cancha_id is None:
            return

        cancha = self.db.query(Canchas).filter(Canchas.id == cancha_id).first()
        if cancha is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cancha seleccionada no existe.",
            )

    def create(self, data):
        self._validate_cancha(data.cancha_id)
        return super().create(data)

    def update(self, item_id, data):
        if "cancha_id" in data.model_dump(exclude_unset=True):
            self._validate_cancha(data.cancha_id)
        return super().update(item_id, data)
