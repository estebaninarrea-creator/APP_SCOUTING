from app.database import engine
from app.models import Base

print("Creando tablas...")

Base.metadata.create_all(bind=engine)

print("Proceso finalizado.")
