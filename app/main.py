from fastapi import Depends, FastAPI, Request, Response
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.dependencies import require_permissions

from app.routers.arbitros import router as arbitros_router
from app.routers.auth import router as auth_router
from app.routers.categorias import router as categorias_router
from app.routers.canchas import router as canchas_router
from app.routers.clubes import router as clubes_router
from app.routers.criterios_evaluacion import router as criterios_evaluacion_router
from app.routers.dashboard import router as dashboard_router
from app.routers.equipos import router as equipos_router
from app.routers.estadios import router as estadios_router
from app.routers.estados import router as estados_router
from app.routers.formaciones import router as formaciones_router
from app.routers.formacion_jugadores import router as formacion_jugadores_router
from app.routers.health import router as health_router
from app.routers.jugadores import router as jugadores_router
from app.routers.ligas import router as ligas_router
from app.routers.maestros import router as maestros_router
from app.routers.partidos import router as partidos_router
from app.routers.partido_jugadores import router as partido_jugadores_router
from app.routers.planteles import router as planteles_router
from app.routers.rol import router as rol_router
from app.routers.tipos_torneo import router as tipos_torneo_router
from app.routers.scouting import router as scouting_router
from app.routers.scouts import router as scouts_router
from app.routers.temporadas import router as temporadas_router
from app.routers.torneos import router as torneos_router
from app.routers.torneos_clubes import router as torneos_clubes_router
from app.routers.usuarios import router as usuarios_router
from app.routers.usuarios_ligas import router as usuarios_ligas_router


app = FastAPI(
    title="Scouting App API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
admin_manage = [Depends(require_permissions("admin:manage"))]
jugadores_view = [Depends(require_permissions("jugadores:view"))]
equipos_view = [Depends(require_permissions("equipos:view"))]
planteles_view = [Depends(require_permissions("planteles:view"))]
partidos_view = [Depends(require_permissions("partidos:view"))]
torneos_view = [Depends(require_permissions("torneos:view"))]
scouting_view = [Depends(require_permissions("scouting:view"))]
scouts_view = [Depends(require_permissions("scouts:view"))]
dashboard_view = [Depends(require_permissions("dashboard:view"))]

app.include_router(arbitros_router, dependencies=admin_manage)
app.include_router(auth_router)
app.include_router(canchas_router, dependencies=admin_manage)
app.include_router(categorias_router, dependencies=admin_manage)
app.include_router(clubes_router, dependencies=admin_manage)
app.include_router(criterios_evaluacion_router, dependencies=admin_manage)
app.include_router(dashboard_router, dependencies=dashboard_view)
app.include_router(equipos_router, dependencies=equipos_view)
app.include_router(estadios_router, dependencies=admin_manage)
app.include_router(estados_router, dependencies=admin_manage)
app.include_router(formacion_jugadores_router, dependencies=admin_manage)
app.include_router(formaciones_router, dependencies=admin_manage)
app.include_router(health_router)
app.include_router(jugadores_router, dependencies=jugadores_view)
app.include_router(ligas_router, dependencies=admin_manage)
app.include_router(maestros_router, dependencies=admin_manage)
app.include_router(partidos_router, dependencies=partidos_view)
app.include_router(partido_jugadores_router, dependencies=partidos_view)
app.include_router(planteles_router, dependencies=planteles_view)
app.include_router(rol_router, dependencies=admin_manage)
app.include_router(scouting_router, dependencies=scouting_view)
app.include_router(scouts_router, dependencies=scouts_view)
app.include_router(temporadas_router, dependencies=admin_manage)
app.include_router(tipos_torneo_router, dependencies=admin_manage)
app.include_router(torneos_router, dependencies=torneos_view)
app.include_router(torneos_clubes_router, dependencies=admin_manage)
app.include_router(usuarios_router, dependencies=admin_manage)
app.include_router(usuarios_ligas_router, dependencies=admin_manage)


@app.get("/")
def root():
    return {
        "app": "Scouting App",
        "version": "1.0.0",
        "status": "OK"
    }


@app.options("/{path:path}")
async def options_handler(request: Request):
    origin = request.headers.get("origin")
    response = Response(status_code=200)
    if origin:
        response.headers["access-control-allow-origin"] = origin
        response.headers["access-control-allow-credentials"] = "true"
        response.headers["access-control-allow-methods"] = "*"
        response.headers["access-control-allow-headers"] = "*"
    return response


@app.get("/health/database")
def health_database():

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:

        return {
            "database": "error",
            "detail": str(e)
        }
