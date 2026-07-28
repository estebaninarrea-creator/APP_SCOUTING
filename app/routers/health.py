from fastapi import APIRouter
from app.database import check_database_connection


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/database")
def health_database():

    connected = check_database_connection()

    if connected:
        return {
            "database": "ok",
            "message": "PostgreSQL conectado correctamente"
        }

    return {
        "database": "error",
        "message": "No se pudo conectar a PostgreSQL"
    }
