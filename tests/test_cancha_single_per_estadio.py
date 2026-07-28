from datetime import date
from uuid import uuid4

from app.database import SessionLocal
from app.models.categoria import Categorias
from app.models.ciudad import Ciudades
from app.models.club import Clubes
from app.models.estadio import Estadios
from app.models.liga import Ligas
from app.models.pais import Paises
from app.models.provincia import Provincias
from app.models.temporada import Temporadas


def _build_estadio_for_cancha_test() -> dict[str, str]:
    suffix = uuid4().hex[:8]
    db = SessionLocal()
    try:
        pais = db.query(Paises).filter(Paises.codigo_iso2 == "TT").first()
        if not pais:
            pais = Paises(nombre=f"Pais Test {suffix}", codigo_iso2="TT", codigo_iso3="TST", codigo_fifa="TST")
            db.add(pais)
            db.flush()

        provincia = Provincias(nombre=f"Provincia Test {suffix}", pais_id=pais.id)
        db.add(provincia)
        db.flush()

        ciudad = Ciudades(nombre=f"Ciudad Test {suffix}", provincia_id=provincia.id)
        db.add(ciudad)
        db.flush()

        liga = db.query(Ligas).order_by(Ligas.created_at.desc()).first()
        if not liga:
            liga = Ligas(nombre=f"Liga Cancha {suffix}", pais_id=pais.id, provincia_id=provincia.id)
            db.add(liga)
            db.flush()

        temporada = db.query(Temporadas).filter(Temporadas.liga_id == liga.id).first()
        if not temporada:
            temporada = Temporadas(
                liga_id=liga.id,
                nombre=f"TEMP-CAN-{suffix}",
                fecha_inicio=date(2033, 1, 1),
                fecha_fin=date(2033, 12, 31),
                activa=False,
            )
            db.add(temporada)
            db.flush()

        categoria = db.query(Categorias).order_by(Categorias.created_at.asc()).first()
        if not categoria:
            categoria = Categorias(nombre=f"CAT-CAN-{suffix}", sexo="M")
            db.add(categoria)
            db.flush()

        club = Clubes(nombre=f"Club Cancha {suffix}", ciudad_id=ciudad.id)
        db.add(club)
        db.flush()

        estadio = Estadios(club_id=club.id, nombre=f"Estadio Cancha {suffix}", ciudad_id=ciudad.id)
        db.add(estadio)
        db.commit()

        return {"estadio_id": str(estadio.id)}
    finally:
        db.close()


def test_cannot_create_second_cancha_for_same_estadio(client):
    entities = _build_estadio_for_cancha_test()

    first = client.post(
        "/canchas/",
        json={
            "estadio_id": entities["estadio_id"],
            "nombre": "Cancha Principal",
            "tipo_superficie": "cesped natural",
            "iluminacion": True,
            "habilitada": True,
        },
    )
    assert first.status_code == 201

    second = client.post(
        "/canchas/",
        json={
            "estadio_id": entities["estadio_id"],
            "nombre": "Cancha 2",
            "tipo_superficie": "tierra",
            "iluminacion": False,
            "habilitada": True,
        },
    )
    assert second.status_code == 400
    assert "Ya existe una cancha para este estadio" in second.json()["detail"]