from app.database import SessionLocal
from app.models.club import Clubes
from app.models.equipo import Equipos
from sqlalchemy import inspect

db = SessionLocal()
try:
    club = db.query(Clubes).filter(Clubes.id=='7f65959c-5f98-4c28-8c2e-6327ba499eb7').first()
    print('club found', club)
    print('related equipos', db.query(Equipos).filter(Equipos.club_id==club.id).count())
    print('table exists', inspect(db.bind).has_table('equipos'))
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    db.close()
