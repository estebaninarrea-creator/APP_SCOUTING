import urllib.request, json, sys

base_url = "http://127.0.0.1:8010"
endpoints = [
    ("/jugadores/", "Jugadores"),
    ("/maestros/", "Maestros"),
    ("/torneos/", "Torneos"),
    ("/ligas/", "Ligas"),
    ("/temporadas/", "Temporadas"),
    ("/categorias/", "Categorías"),
    ("/tipos_torneo/", "Tipos de Torneo"),
    ("/clubes/", "Clubes"),
    ("/equipos/", "Equipos"),
    ("/partidos/", "Partidos"),
    ("/roles/", "Roles"),
    ("/usuarios/", "Usuarios"),
]

print("=" * 70)
print("DIAGNÓSTICO DE ENDPOINTS DEL API")
print("=" * 70)

for endpoint, name in endpoints:
    try:
        req = urllib.request.Request(
            base_url + endpoint,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                if 'provincias' in data:
                    count = f"provincias:{len(data.get('provincias',[]))} ciudades:{len(data.get('ciudades',[]))} posiciones:{len(data.get('posiciones',[]))}"
                else:
                    count = len(data)
            else:
                count = "?"
            
            status = "✅" if (isinstance(count, int) and count > 0) or (isinstance(count, str) and "0" not in count) else "⚠️"
            print(f"{status} {name:20} | {endpoint:30} | Count: {count}")
    except Exception as e:
        print(f"❌ {name:20} | {endpoint:30} | Error: {str(e)[:50]}")

print("=" * 70)
