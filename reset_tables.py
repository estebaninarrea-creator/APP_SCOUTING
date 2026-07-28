"""
Script para dropear y recrear todas las tablas de la base de datos.
"""

from sqlalchemy import text
from app.database import engine
from app.models import Base

print("Dropeando todas las vistas...")

# Dropear vistas explícitamente
views_to_drop = [
    'vw_evaluaciones_jugador',
    'vw_fixture_torneo',
    'vw_historial_jugador',
    'vw_jugador_partidos',
    'vw_jugadores',
    'vw_planteles_actuales',
    'vw_potencial_jugadores'
]

with engine.connect() as conn:
    for view_name in views_to_drop:
        try:
            conn.execute(text(f"DROP VIEW IF EXISTS {view_name} CASCADE"))
            print(f"  ✓ Vista {view_name} dropeada")
        except Exception as e:
            print(f"  ⚠ Error dropeando {view_name}: {e}")
    conn.commit()

print("\nDropeando todas las tablas...")
Base.metadata.drop_all(bind=engine)
print("✅ Tablas dropeadas.")

print("\nCreando todas las tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas.")

print("\n✅ Base de datos reiniciada correctamente.")
