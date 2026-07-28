from app.dependencies import get_db
from app.services.jugador_service import get_jugadores
from app.services.maestros_service import get_datos_maestros

db = next(get_db())
print('jugadores', len(get_jugadores(db)))
print('maestros', len(get_datos_maestros(db)['posiciones']))
