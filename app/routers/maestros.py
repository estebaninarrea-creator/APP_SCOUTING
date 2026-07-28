from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.maestros import (
    CiudadCreate,
    CiudadResponse,
    CiudadUpdate,
    DatosMaestrosResponse,
    PaisCreate,
    PaisResponse,
    PaisUpdate,
    PosicionCreate,
    PosicionResponse,
    PosicionUpdate,
    ProvinciaCreate,
    ProvinciaResponse,
    ProvinciaUpdate,
)
from app.services.maestros_service import (
    create_ciudad,
    create_pais,
    create_posicion,
    create_provincia,
    create_provincias_bulk,
    delete_ciudad,
    delete_pais,
    delete_posicion,
    delete_provincia,
    get_ciudad,
    get_ciudades,
    get_datos_maestros,
    get_pais,
    get_paises,
    get_posicion,
    get_posiciones,
    get_provincia,
    get_provincias,
    update_ciudad,
    update_pais,
    update_posicion,
    update_provincia,
)

router = APIRouter(prefix="/maestros", tags=["Datos Maestros"])


@router.get("/", response_model=DatosMaestrosResponse)
def listar_datos_maestros(db: Session = Depends(get_db)):
    try:
        data = get_datos_maestros(db)
        return {
            "provincias": [
                {
                    "id": item.id,
                    "nombre": item.nombre,
                    "pais_id": item.pais_id,
                }
                for item in data["provincias"]
            ],
            "ciudades": [
                {
                    "id": item.id,
                    "nombre": item.nombre,
                    "provincia_id": item.provincia_id,
                }
                for item in data["ciudades"]
            ],
            "posiciones": [
                {
                    "id": item.id,
                    "codigo": item.codigo,
                    "nombre": item.nombre,
                    "orden": item.orden,
                }
                for item in data["posiciones"]
            ],
            "temporadas": [
                {
                    "id": item.id,
                    "nombre": item.nombre,
                }
                for item in data["temporadas"]
            ],
            "categorias": [
                {
                    "id": item.id,
                    "nombre": item.nombre,
                }
                for item in data["categorias"]
            ],
            "tipos_torneo": [
                {
                    "id": item.id,
                    "nombre": item.nombre,
                }
                for item in data["tipos_torneo"]
            ],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al cargar datos maestros: {exc}") from exc


@router.get("/paises", response_model=list[PaisResponse])
def listar_paises(db: Session = Depends(get_db)):
    return get_paises(db)


@router.post("/paises", response_model=PaisResponse)
def crear_pais(pais: PaisCreate, db: Session = Depends(get_db)):
    return create_pais(db, pais)


@router.get("/paises/{pais_id}", response_model=PaisResponse)
def obtener_pais(pais_id: UUID, db: Session = Depends(get_db)):
    pais = get_pais(db, pais_id)
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return pais


@router.put("/paises/{pais_id}", response_model=PaisResponse)
def actualizar_pais(pais_id: UUID, pais: PaisUpdate, db: Session = Depends(get_db)):
    updated = update_pais(db, pais_id, pais)
    if not updated:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return updated


@router.delete("/paises/{pais_id}")
def eliminar_pais(pais_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_pais(db, pais_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return {"mensaje": "País eliminado"}


@router.get("/provincias", response_model=list[ProvinciaResponse])
def listar_provincias(db: Session = Depends(get_db)):
    return get_provincias(db)


@router.post("/provincias", response_model=ProvinciaResponse)
def crear_provincia(provincia: ProvinciaCreate, db: Session = Depends(get_db)):
    return create_provincia(db, provincia)


@router.post("/provincias/bulk", response_model=list[ProvinciaResponse])
def crear_provincias_bulk_endpoint(provincias: list[ProvinciaCreate] | None = None, db: Session = Depends(get_db)):
    return create_provincias_bulk(db, provincias)


@router.get("/provincias/{provincia_id}", response_model=ProvinciaResponse)
def obtener_provincia(provincia_id: UUID, db: Session = Depends(get_db)):
    provincia = get_provincia(db, provincia_id)
    if not provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return provincia


@router.put("/provincias/{provincia_id}", response_model=ProvinciaResponse)
def actualizar_provincia(provincia_id: UUID, provincia: ProvinciaUpdate, db: Session = Depends(get_db)):
    updated = update_provincia(db, provincia_id, provincia)
    if not updated:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return updated


@router.delete("/provincias/{provincia_id}")
def eliminar_provincia(provincia_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = delete_provincia(db, provincia_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=409, detail="No se puede eliminar la provincia porque tiene datos relacionados") from exc

    if not deleted:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return {"mensaje": "Provincia eliminada"}


@router.get("/ciudades", response_model=list[CiudadResponse])
def listar_ciudades(db: Session = Depends(get_db)):
    return get_ciudades(db)


@router.post("/ciudades", response_model=CiudadResponse)
def crear_ciudad(ciudad: CiudadCreate, db: Session = Depends(get_db)):
    return create_ciudad(db, ciudad)


@router.get("/ciudades/{ciudad_id}", response_model=CiudadResponse)
def obtener_ciudad(ciudad_id: UUID, db: Session = Depends(get_db)):
    ciudad = get_ciudad(db, ciudad_id)
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return ciudad


@router.put("/ciudades/{ciudad_id}", response_model=CiudadResponse)
def actualizar_ciudad(ciudad_id: UUID, ciudad: CiudadUpdate, db: Session = Depends(get_db)):
    updated = update_ciudad(db, ciudad_id, ciudad)
    if not updated:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return updated


@router.delete("/ciudades/{ciudad_id}")
def eliminar_ciudad(ciudad_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = delete_ciudad(db, ciudad_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=409, detail="No se puede eliminar la ciudad porque tiene datos relacionados") from exc

    if not deleted:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return {"mensaje": "Ciudad eliminada"}


@router.get("/posiciones", response_model=list[PosicionResponse])
def listar_posiciones(db: Session = Depends(get_db)):
    return get_posiciones(db)


@router.post("/posiciones", response_model=PosicionResponse)
def crear_posicion(posicion: PosicionCreate, db: Session = Depends(get_db)):
    return create_posicion(db, posicion)


@router.get("/posiciones/{posicion_id}", response_model=PosicionResponse)
def obtener_posicion(posicion_id: UUID, db: Session = Depends(get_db)):
    posicion = get_posicion(db, posicion_id)
    if not posicion:
        raise HTTPException(status_code=404, detail="Posición no encontrada")
    return posicion


@router.put("/posiciones/{posicion_id}", response_model=PosicionResponse)
def actualizar_posicion(posicion_id: UUID, posicion: PosicionUpdate, db: Session = Depends(get_db)):
    updated = update_posicion(db, posicion_id, posicion)
    if not updated:
        raise HTTPException(status_code=404, detail="Posición no encontrada")
    return updated


@router.delete("/posiciones/{posicion_id}")
def eliminar_posicion(posicion_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_posicion(db, posicion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Posición no encontrada")
    return {"mensaje": "Posición eliminada"}
