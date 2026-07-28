from app.models.criterio_evaluacion import CriteriosEvaluacion
from app.services.crud_service import CRUDService


class CriterioEvaluacionService(CRUDService):
    def __init__(self, db):
        super().__init__(db, CriteriosEvaluacion)
