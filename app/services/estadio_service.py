from app.models.estadio import Estadios
from app.services.crud_service import CRUDService


class EstadioService(CRUDService):
    def __init__(self, db):
        super().__init__(db, Estadios)
