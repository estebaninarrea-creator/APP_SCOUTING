#!/usr/bin/env python3
"""
Limpia los datos operativos de prueba y carga clubes/equipos reales de la
Liga Cultural de La Pampa.

Conserva las tablas maestras, roles, usuarios y scouts.

Uso:
    c:/Futbol/Proyecto/ScoutingApp/backend/venv/Scripts/python.exe seed_real_data.py
"""

from __future__ import annotations

from datetime import date
import unicodedata

from sqlalchemy import delete, select
from sqlalchemy import text

from app.database import SessionLocal
from app.models import (
    Base,
    Categorias,
    Ciudades,
    Clubes,
    Equipos,
    Ligas,
    Paises,
    Provincias,
    Temporadas,
)


KEEP_TABLES = {
    "roles",
    "paises",
    "provincias",
    "ciudades",
    "categorias",
    "estados",
    "posiciones",
    "tipos_torneo",
    "temporadas",
    "criterios_evaluacion",
    "usuarios",
    "scouts",
}

REAL_LEAGUE_NAME = "Liga Cultural de La Pampa"
REAL_SEASON_NAME = "2026"


REAL_CLUBS = [
    ("All Boys", "Santa Rosa"),
    ("Atlético Santa Rosa", "Santa Rosa"),
    ("General Belgrano", "Santa Rosa"),
    ("La Barranca", "Santa Rosa"),
    ("Deportivo Mac Allister", "Santa Rosa"),
    ("Deportivo Winifreda", "Winifreda"),
    ("Unión Deportiva Campos", "General Acha"),
    ("Atlético Macachín", "Macachín"),
    ("Unión Deportiva Riglos", "Miguel Riglos"),
    ("El Pampero", "Colonia Santa María"),
    ("Unión Acha", "General Acha"),
    ("Deportivo Centro Oeste", "Santa Rosa"),
    ("Deportivo Carro Quemado", "Carro Quemado"),
    ("Sarmiento", "Santa Rosa"),
    ("Guardia del Monte", "Toay"),
    ("Penales", "Santa Rosa"),
    ("Deportivo Uriburu", "Uriburu"),
    ("Juventud Unida", "Santa Isabel"),
    ("Matadero por la Lealtad", "Santa Rosa"),
    ("Deportivo Telén", "Telén"),
    ("Sportivo Luan Toro", "Luan Toro"),
    ("Santa María", "Santa Rosa"),
    ("Matadero", "Santa Rosa"),
    ("Cochico", "Victorica"),
]


def make_sigla(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name)
    words = []
    for word in normalized.split():
        clean_word = "".join(character for character in word if character.isalpha())
        if clean_word:
            words.append(clean_word)

    sigla = "".join(word[0] for word in words).upper()
    if not sigla:
        sigla = "EQ"
    if len(sigla) == 1:
        sigla = f"{sigla}X"
    return sigla[:10]


def clear_operational_data(session) -> None:
    print("\nLimpiando tablas operativas...")
    tables_to_truncate = [
        table.name
        for table in Base.metadata.sorted_tables
        if table.name not in KEEP_TABLES
    ]
    if not tables_to_truncate:
        return

    quoted_tables = ", ".join(f'"{table_name}"' for table_name in tables_to_truncate)
    session.execute(text(f"TRUNCATE TABLE {quoted_tables} RESTART IDENTITY CASCADE"))


def remove_test_master_data(session) -> None:
    print("Limpiando maestros de prueba...")
    session.execute(delete(Ciudades).where(Ciudades.nombre.like("Ciudad Test%")))
    session.execute(delete(Provincias).where(Provincias.nombre.like("Provincia Test%")))


def get_or_create_country(session) -> Paises:
    country = session.execute(
        select(Paises).where(Paises.nombre == "Argentina")
    ).scalars().first()
    if country:
        return country

    country = Paises(nombre="Argentina", codigo_iso2="AR", codigo_iso3="ARG", codigo_fifa="ARG")
    session.add(country)
    session.flush()
    return country


def get_or_create_province(session, country: Paises, name: str) -> Provincias:
    province = session.execute(
        select(Provincias).where(Provincias.nombre == name)
    ).scalars().first()
    if province:
        return province

    province = Provincias(nombre=name, pais_id=country.id)
    session.add(province)
    session.flush()
    return province


def get_or_create_city(session, province: Provincias, name: str) -> Ciudades:
    city = session.execute(
        select(Ciudades).where(
            Ciudades.nombre == name,
            Ciudades.provincia_id == province.id,
        )
    ).scalars().first()
    if city:
        return city

    city = Ciudades(nombre=name, provincia_id=province.id)
    session.add(city)
    session.flush()
    return city


def get_primary_category(session) -> Categorias:
    category = session.execute(
        select(Categorias).where(Categorias.nombre.ilike("Primera%"))
    ).scalars().first()
    if not category:
        raise RuntimeError("No se encontró una categoría de Primera para crear los equipos")
    return category


def get_or_create_league(session, country: Paises, province: Provincias) -> Ligas:
    league = session.execute(
        select(Ligas).where(Ligas.nombre == REAL_LEAGUE_NAME)
    ).scalars().first()
    if league:
        league.pais_id = country.id
        league.provincia_id = province.id
        league.activo = True
        return league

    league = Ligas(
        nombre=REAL_LEAGUE_NAME,
        pais_id=country.id,
        provincia_id=province.id,
        activo=True,
    )
    session.add(league)
    session.flush()
    return league


def get_or_create_season(session, league: Ligas) -> Temporadas:
    season = session.execute(
        select(Temporadas).where(
            Temporadas.liga_id == league.id,
            Temporadas.nombre == REAL_SEASON_NAME,
        )
    ).scalars().first()
    if season:
        season.activa = True
        return season

    season = Temporadas(
        liga_id=league.id,
        nombre=REAL_SEASON_NAME,
        fecha_inicio=date(2026, 3, 1),
        fecha_fin=date(2026, 12, 15),
        activa=True,
    )
    session.add(season)
    session.flush()
    return season


def seed_real_clubs_and_teams(session) -> None:
    print("Cargando provincia y ciudades reales...")
    country = get_or_create_country(session)
    lapampa = get_or_create_province(session, country, "La Pampa")
    league = get_or_create_league(session, country, lapampa)

    city_cache: dict[str, Ciudades] = {}
    for _, city_name in REAL_CLUBS:
        if city_name not in city_cache:
            city_cache[city_name] = get_or_create_city(session, lapampa, city_name)

    category = get_primary_category(session)
    season = get_or_create_season(session, league)

    print("Cargando clubes y equipos...")
    for club_name, city_name in REAL_CLUBS:
        city = city_cache[city_name]

        club = session.execute(
            select(Clubes).where(Clubes.nombre == club_name)
        ).scalars().first()
        if not club:
            club = Clubes(
                nombre=club_name,
                activo=True,
                ciudad_id=city.id,
                nombre_corto=club_name,
                sigla=make_sigla(club_name),
            )
            session.add(club)
            session.flush()
        elif club.ciudad_id != city.id:
            club.ciudad_id = city.id

        team = session.execute(
            select(Equipos).where(
                Equipos.club_id == club.id,
                Equipos.temporada_id == season.id,
                Equipos.categoria_id == category.id,
            )
        ).scalars().first()
        if not team:
            team = Equipos(
                club_id=club.id,
                temporada_id=season.id,
                categoria_id=category.id,
                nombre=club_name,
            )
            session.add(team)

        print(f"  OK {club_name} -> {city_name}")


def main() -> None:
    print("=" * 72)
    print("RESET Y CARGA REAL - LIGA CULTURAL DE LA PAMPA")
    print("=" * 72)

    session = SessionLocal()
    try:
        clear_operational_data(session)
        remove_test_master_data(session)
        seed_real_clubs_and_teams(session)
        session.commit()
        print("\nProceso finalizado correctamente.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()