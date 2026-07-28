from datetime import date
from uuid import uuid4

from app.models.cancha import Canchas
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

        cancha = Canchas(nombre=f"Cesped sintetico {suffix}", descripcion="Cancha principal de prueba")
        db.add(cancha)
        db.flush()

        estadio = Estadios(club_id=club.id, nombre=f"Estadio Cancha {suffix}", ciudad_id=ciudad.id, cancha_id=cancha.id)
        db.add(estadio)
        db.commit()

        return {"estadio_id": str(estadio.id), "cancha_id": str(cancha.id)}
    finally:
        db.close()


def test_cancha_catalog_can_be_created_without_estadio(client):
    response = client.post(
        "/canchas/",
        json={
            "nombre": f"Cesped natural {uuid4().hex[:6]}",
            "descripcion": "Catalogo de tipo de cancha",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["nombre"]
    assert "estadio_id" not in body


def test_estadio_can_store_cancha_relation(client):
    entities = _build_estadio_for_cancha_test()

    response = client.get(f"/estadios/{entities['estadio_id']}")
    assert response.status_code == 200
    assert response.json()["cancha_id"] == entities["cancha_id"]


def test_estadio_rejects_invalid_cancha_id(client):
    entities = _build_estadio_for_cancha_test()

    response = client.put(
        f"/estadios/{entities['estadio_id']}",
        json={
            "cancha_id": str(uuid4()),
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "La cancha seleccionada no existe."