from fastapi import HTTPException, status
from sqlalchemy import or_

from app.models.formacion import Formaciones
from app.models.formacion_jugador import FormacionJugadores
from app.models.jugador import Jugadores
from app.models.plantel import Planteles
from app.models.posicion import Posiciones
from app.services.crud_service import CRUDService


class FormacionJugadorService(CRUDService):
    def __init__(self, db):
        super().__init__(db, FormacionJugadores)

    def _validate_assignment(self, formacion_id, jugador_id, posicion_id):
        formacion = self.db.query(Formaciones).filter(Formaciones.id == formacion_id).first()
        if not formacion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formación no encontrada")

        if not formacion.partido:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La formación no tiene partido asociado")

        partido = formacion.partido
        if formacion.equipo_id not in {partido.equipo_local_id, partido.equipo_visitante_id}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La formación debe pertenecer a uno de los equipos del partido",
            )

        jugador = self.db.query(Jugadores).filter(Jugadores.id == jugador_id).first()
        if not jugador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")

        if posicion_id:
            posicion = self.db.query(Posiciones).filter(Posiciones.id == posicion_id).first()
            if not posicion:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posición no encontrada")

        query = self.db.query(Planteles).filter(
            Planteles.equipo_id == formacion.equipo_id,
            Planteles.jugador_id == jugador_id,
            Planteles.activo.is_(True),
        )
        if partido.fecha_partido:
            query = query.filter(
                Planteles.fecha_desde <= partido.fecha_partido,
                or_(Planteles.fecha_hasta.is_(None), Planteles.fecha_hasta >= partido.fecha_partido),
            )
        if not query.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El jugador no pertenece a un plantel activo del equipo en la fecha del partido",
            )

    def create(self, data):
        self._validate_assignment(data.formacion_id, data.jugador_id, data.posicion_id)
        return super().create(data)

    def update(self, item_id, data):
        existing = self.get(item_id)
        if data.posicion_id is not None:
            posicion = self.db.query(Posiciones).filter(Posiciones.id == data.posicion_id).first()
            if not posicion:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posición no encontrada")

        # Valida consistencia vigente de la asignación antes de persistir cambios.
        effective_posicion_id = data.posicion_id if data.posicion_id is not None else existing.posicion_id
        self._validate_assignment(existing.formacion_id, existing.jugador_id, effective_posicion_id)
        return super().update(item_id, data)
