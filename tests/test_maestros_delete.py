from app.database import SessionLocal
from app.models.ciudad import Ciudades
from app.models.pais import Paises
from app.models.provincia import Provincias


def test_delete_provincia_blocked_when_related_city_exists(client):
    db = SessionLocal()
    try:
        pais = db.query(Paises).order_by(Paises.nombre).first()
        if not pais:
            pais = Paises(nombre='Argentina', codigo_iso2='AR', codigo_iso3='ARG', codigo_fifa='ARG')
            db.add(pais)
            db.commit()
            db.refresh(pais)

        provincia = Provincias(nombre='Provincia Test Delete', pais_id=pais.id)
        db.add(provincia)
        db.commit()
        db.refresh(provincia)

        ciudad = Ciudades(nombre='Ciudad Test Delete', provincia_id=provincia.id)
        db.add(ciudad)
        db.commit()
        db.refresh(ciudad)

        response = client.delete(f'/maestros/provincias/{provincia.id}')

        assert response.status_code == 409
        assert response.json()['detail'] == 'No se puede eliminar la provincia porque tiene ciudades o ligas relacionadas'
        assert db.query(Provincias).filter(Provincias.id == provincia.id).first() is not None
        assert db.query(Ciudades).filter(Ciudades.id == ciudad.id).first() is not None
    finally:
        db.close()
