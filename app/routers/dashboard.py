from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.club import Clubes
from app.models.jugador import Jugadores
from app.models.partido import Partidos
from app.models.rol import Roles

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    return {
        "jugadores": db.query(Jugadores).count(),
        "roles": db.query(Roles).count(),
        "partidos": db.query(Partidos).count(),
        "clubes": db.query(Clubes).count(),
    }
