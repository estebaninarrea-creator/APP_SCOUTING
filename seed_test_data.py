#!/usr/bin/env python3
"""
Script de inicialización de datos de prueba para Scouting App
Crea datos maestros básicos y algunos registros de ejemplo

Uso:
    python seed_test_data.py

Este script:
✅ Crea provincias de ejemplo
✅ Crea ciudades con sus provincias
✅ Crea posiciones de futbolista
✅ Crea roles de usuario
✅ Crea jugadores de ejemplo
✅ Crea equipos de ejemplo
✅ Crea partidos de ejemplo
"""

import urllib.request
import urllib.error
import json
import sys
from datetime import datetime, timedelta

from app.core.security import hash_password

BASE_URL = "http://127.0.0.1:8010"

def make_request(method, endpoint, payload=None):
    """Hacer petición HTTP al API"""
    url = BASE_URL + endpoint
    headers = {'Content-Type': 'application/json'}
    
    try:
        if payload:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result, response.status
    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read().decode())
        except (json.JSONDecodeError, Exception):
            error_data = {"error": f"HTTP {e.code}", "raw": e.read().decode()[:100]}
        return error_data, e.code
    except Exception as e:
        return {"error": str(e)}, 500

def seed_provincias():
    """Crear provincias"""
    print("\n📍 Creando provincias...")
    provincias = [
        {"nombre": "Buenos Aires", "pais_id": None},
        {"nombre": "Córdoba", "pais_id": None},
        {"nombre": "Santa Fe", "pais_id": None},
        {"nombre": "Mendoza", "pais_id": None},
        {"nombre": "San Juan", "pais_id": None},
    ]
    
    ids = {}
    for prov in provincias:
        result, status = make_request("POST", "/maestros/provincias", prov)
        if status == 201 or status == 200:
            ids[prov["nombre"]] = result["id"]
            print(f"  ✅ {prov['nombre']}: {result['id']}")
        else:
            print(f"  ❌ {prov['nombre']}: {result}")
    
    return ids

def seed_ciudades(provincia_ids):
    """Crear ciudades"""
    print("\n🏙️  Creando ciudades...")
    ciudades = [
        {"nombre": "La Plata", "provincia_id": provincia_ids.get("Buenos Aires"), "codigo_postal": "1900"},
        {"nombre": "Capital Federal", "provincia_id": provincia_ids.get("Buenos Aires"), "codigo_postal": "1001"},
        {"nombre": "Córdoba Capital", "provincia_id": provincia_ids.get("Córdoba"), "codigo_postal": "5000"},
        {"nombre": "Rosario", "provincia_id": provincia_ids.get("Santa Fe"), "codigo_postal": "2000"},
        {"nombre": "Mendoza Capital", "provincia_id": provincia_ids.get("Mendoza"), "codigo_postal": "5500"},
    ]
    
    ids = {}
    for ciudad in ciudades:
        if not ciudad["provincia_id"]:
            print(f"  ⚠️  {ciudad['nombre']}: Provincia no encontrada")
            continue
        
        result, status = make_request("POST", "/maestros/ciudades", ciudad)
        if status == 201 or status == 200:
            ids[ciudad["nombre"]] = result["id"]
            print(f"  ✅ {ciudad['nombre']}: {result['id']}")
        else:
            print(f"  ❌ {ciudad['nombre']}: {result}")
    
    return ids

def seed_posiciones():
    """Crear posiciones de futbolista"""
    print("\n⚽ Creando posiciones...")
    posiciones = [
        {"codigo": "PT", "nombre": "Portero", "orden": 1},
        {"codigo": "DEF", "nombre": "Defensa", "orden": 2},
        {"codigo": "CC", "nombre": "Centrocampista", "orden": 3},
        {"codigo": "DL", "nombre": "Delantero", "orden": 4},
        {"codigo": "EXD", "nombre": "Extremo Derecho", "orden": 5},
        {"codigo": "EXI", "nombre": "Extremo Izquierdo", "orden": 6},
    ]
    
    ids = {}
    for pos in posiciones:
        result, status = make_request("POST", "/maestros/posiciones", pos)
        if status == 201 or status == 200:
            ids[pos["nombre"]] = result["id"]
            print(f"  ✅ {pos['nombre']}: {result['id']}")
        else:
            print(f"  ❌ {pos['nombre']}: {result}")
    
    return ids

def seed_roles():
    """Crear roles de usuario"""
    print("\n👤 Creando roles...")
    roles = [
        {"nombre": "Admin", "descripcion": "Administrador del sistema"},
        {"nombre": "Scout", "descripcion": "Scout o cazador de talentos"},
        {"nombre": "Entrenador", "descripcion": "Entrenador o preparador físico"},
        {"nombre": "Usuario", "descripcion": "Usuario estándar"},
    ]
    
    ids = {}
    for role in roles:
        result, status = make_request("POST", "/roles/", role)
        if status == 201 or status == 200:
            ids[role["nombre"]] = result["id"]
            print(f"  ✅ {role['nombre']}: {result['id']}")
        else:
            print(f"  ⚠️  {role['nombre']}: Posiblemente ya existe")
            # Buscar el role existente
            roles_data, _ = make_request("GET", "/roles/", None)
            if isinstance(roles_data, list):
                for r in roles_data:
                    if r.get("nombre") == role["nombre"]:
                        ids[role["nombre"]] = r["id"]
                        break
    
    return ids


def seed_admin_user(role_ids):
    """Crear usuario admin de prueba"""
    print("\n🔐 Creando usuario admin de prueba...")

    admin_payload = {
        "rol_id": role_ids.get("Admin"),
        "nombre": "Admin",
        "apellido": "Sistema",
        "email": "admin@example.com",
        "password_hash": hash_password("Admin1234!"),
        "activo": True,
    }

    if not admin_payload["rol_id"]:
        print("  ❌ Rol Admin no encontrado")
        return None

    result, status = make_request("POST", "/usuarios/", admin_payload)
    if status == 201 or status == 200:
        print(f"  ✅ admin@example.com: {result['id']}")
        return result["id"]

    print(f"  ⚠️  admin@example.com: {result}")
    return None

def seed_clubes():
    """Crear clubes de ejemplo"""
    print("\n🏆 Creando clubes...")
    clubes = [
        {"nombre": "Boca Juniors", "codigo": "BJDP"},
        {"nombre": "River Plate", "codigo": "RPDP"},
        {"nombre": "San Lorenzo", "codigo": "SLBA"},
        {"nombre": "Independiente", "codigo": "IDBA"},
    ]
    
    ids = {}
    for club in clubes:
        result, status = make_request("POST", "/clubes/", club)
        if status == 201 or status == 200:
            ids[club["nombre"]] = result["id"]
            print(f"  ✅ {club['nombre']}: {result['id']}")
        else:
            print(f"  ⚠️  {club['nombre']}: {result}")
    
    return ids

def seed_jugadores():
    """Crear jugadores de ejemplo"""
    print("\n👕 Creando jugadores de ejemplo...")
    
    jugadores = [
        {
            "nombre": "Juan",
            "apellido": "Pérez",
            "documento": "12345678",
            "tipo_documento": "DNI",
            "fecha_nacimiento": "2005-01-15",
            "pierna": "derecha",
            "nacionalidad": "Argentino"
        },
        {
            "nombre": "Carlos",
            "apellido": "López",
            "documento": "87654321",
            "tipo_documento": "DNI",
            "fecha_nacimiento": "2004-06-20",
            "pierna": "izquierda",
            "nacionalidad": "Argentino"
        },
        {
            "nombre": "Diego",
            "apellido": "Martínez",
            "documento": "11223344",
            "tipo_documento": "DNI",
            "fecha_nacimiento": "2006-03-10",
            "pierna": "derecha",
            "nacionalidad": "Argentino"
        },
    ]
    
    ids = {}
    for jug in jugadores:
        result, status = make_request("POST", "/jugadores/", jug)
        if status == 201 or status == 200:
            ids[jug["apellido"]] = result["id"]
            print(f"  ✅ {jug['nombre']} {jug['apellido']}: {result['id']}")
        else:
            print(f"  ❌ {jug['nombre']} {jug['apellido']}: {status}")
    
    return ids

def main():
    print("=" * 70)
    print("🌱 INICIALIZANDO DATOS DE PRUEBA - SCOUTING APP")
    print("=" * 70)
    
    # Verificar que backend está disponible
    print("\n🔗 Verificando conexión al backend...")
    result, status = make_request("GET", "/torneos/", None)
    if status != 200:
        print(f"❌ Backend no disponible en {BASE_URL}")
        print(f"   Asegúrate de que está corriendo: python -m uvicorn app.main:app --host 127.0.0.1 --port 8010")
        sys.exit(1)
    print(f"✅ Backend disponible")
    
    # Crear datos maestros
    provincia_ids = seed_provincias()
    ciudad_ids = seed_ciudades(provincia_ids)
    posicion_ids = seed_posiciones()
    role_ids = seed_roles()
    admin_user_id = seed_admin_user(role_ids)
    club_ids = seed_clubes()
    jugador_ids = seed_jugadores()
    
    print("\n" + "=" * 70)
    print("✅ INICIALIZACIÓN COMPLETADA")
    print("=" * 70)
    print(f"""
📊 Datos creados:
  • Provincias:    {len(provincia_ids)}
  • Ciudades:      {len(ciudad_ids)}
  • Posiciones:    {len(posicion_ids)}
  • Roles:         {len(role_ids)}
    • Admin:         {1 if admin_user_id else 0}
  • Clubes:        {len(club_ids)}
  • Jugadores:     {len(jugador_ids)}

🌐 Acceder a:
  • Frontend:  http://127.0.0.1:5173/
  • API Docs:  http://127.0.0.1:8010/docs

🔑 Credenciales de prueba:
    • Email:    admin@example.com
    • Password: Admin1234!

📝 Próximos pasos:
  1. Abrir http://127.0.0.1:5173/
  2. Navegar a /maestros para ver provincias, ciudades, posiciones
  3. Navegar a /jugadores para ver jugadores creados
  4. Crear más registros desde la interfaz
""")

if __name__ == "__main__":
    main()
