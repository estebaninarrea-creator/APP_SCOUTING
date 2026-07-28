from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT c.id
        FROM clubes c
        LEFT JOIN equipos e ON e.club_id = c.id
        LEFT JOIN estadios s ON s.club_id = c.id
        GROUP BY c.id
        HAVING COUNT(DISTINCT e.id) = 0 AND COUNT(DISTINCT s.id) = 0
        LIMIT 10
    """))
    print(rows.fetchall())
