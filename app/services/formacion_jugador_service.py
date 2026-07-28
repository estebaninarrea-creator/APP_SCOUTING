from app.models.formacion_jugador import FormacionJugadores
from app.services.crud_service import CRUDService


class FormacionJugadorService(CRUDService):
    def __init__(self, db):
        super().__init__(db, FormacionJugadores)
