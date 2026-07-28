from app.database import engine
from app.models import Base

print("Modelos cargados correctamente")

Base.metadata.create_all(bind=engine)

print("Tablas verificadas")
