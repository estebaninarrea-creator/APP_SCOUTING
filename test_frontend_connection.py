import json
import urllib.error
import urllib.request


BASE_URL = "http://127.0.0.1:8010"


def _request(method: str, path: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"} if payload else {},
        method=method,
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def run_seed_sequence() -> None:
    liga = _request("POST", "/ligas/", {"nombre": "Liga Provincial", "sitio_web": "", "email": ""})
    temporada = _request(
        "POST",
        "/temporadas/",
        {
            "liga_id": liga["id"],
            "nombre": "Temporada 2024",
            "fecha_inicio": "2024-01-01",
            "fecha_fin": "2024-12-31",
        },
    )
    categoria = _request("POST", "/categorias/", {"nombre": "Primera División"})
    tipo_torneo = _request("POST", "/tipos_torneo/", {"nombre": "Liga"})
    torneo = _request(
        "POST",
        "/torneos/",
        {
            "nombre": "Liga Provincial 2024",
            "temporada_id": temporada["id"],
            "categoria_id": categoria["id"],
            "tipo_torneo_id": tipo_torneo["id"],
        },
    )

    print("Liga creada:", liga["id"])
    print("Temporada creada:", temporada["id"])
    print("Categoria creada:", categoria["id"])
    print("Tipo de torneo creado:", tipo_torneo["id"])
    print("Torneo creado:", torneo["id"])


if __name__ == "__main__":
    try:
        run_seed_sequence()
        print("\nDatos de demo creados correctamente.")
    except urllib.error.HTTPError as err:
        print(f"Error HTTP {err.code}: {err.read().decode()}")
        raise SystemExit(1)
    except Exception as err:
        print(f"Error creando datos: {err}")
        raise SystemExit(1)
