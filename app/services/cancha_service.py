from app.models.cancha import Canchas
from app.services.crud_service import CRUDService


class CanchaService(CRUDService):
    def __init__(self, db):
        super().__init__(db, Canchas)
