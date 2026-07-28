import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from itertools import cycle
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass
class ApiError(Exception):
    status: int | None
    detail: str


class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        body = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if payload is not None:
            body = json.dumps(payload).encode("utf-8")

        req = Request(url=url, method=method.upper(), headers=headers, data=body)

        try:
            with urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                if not raw:
                    return None
                return json.loads(raw)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ApiError(status=exc.code, detail=detail) from exc
        except URLError as exc:
            raise ApiError(status=None, detail=str(exc.reason)) from exc

    def get(self, path: str) -> Any:
        return self._request("GET", path)

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        return self._request("POST", path, payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crea jugadores y los asigna a planteles en round-robin por equipo."
    )
    parser.add_argument("--token", required=True, help="JWT con permisos para crear jugadores y planteles")
    parser.add_argument("--base-url", default="http://127.0.0.1:8010", help="Base URL del backend")
    parser.add_argument("--count", type=int, default=12, help="Cantidad de jugadores a crear")
    parser.add_argument("--fecha-desde", default=str(date.today()), help="Fecha desde para plantel (YYYY-MM-DD)")
    parser.add_argument("--dorsal-inicial", type=int, default=40, help="Primer dorsal para asignar")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    client = ApiClient(args.base_url, args.token)

    try:
        equipos = client.get("/equipos/")
    except ApiError as exc:
        print(json.dumps({"ok": False, "step": "get_equipos", "status": exc.status, "detail": exc.detail}, ensure_ascii=True))
        return 1

    if not isinstance(equipos, list) or not equipos:
        print(json.dumps({"ok": False, "step": "get_equipos", "detail": "No hay equipos disponibles"}, ensure_ascii=True))
        return 1

    created_players: list[dict[str, Any]] = []
    player_errors: list[dict[str, Any]] = []

    for i in range(1, args.count + 1):
        payload = {
            "nombre": f"Seed{i}",
            "apellido": f"Lote{date.today().strftime('%Y%m%d')}",
            "activo": True,
        }
        try:
            created = client.post("/jugadores/", payload)
            created_players.append(created)
        except ApiError as exc:
            player_errors.append({"index": i, "status": exc.status, "detail": exc.detail, "payload": payload})

    if not created_players:
        print(json.dumps({"ok": False, "step": "create_players", "errors": player_errors[:5]}, ensure_ascii=True))
        return 1

    created_rosters: list[dict[str, Any]] = []
    roster_errors: list[dict[str, Any]] = []

    for i, (jugador, equipo) in enumerate(zip(created_players, cycle(equipos)), start=0):
        payload = {
            "equipo_id": equipo["id"],
            "jugador_id": jugador["id"],
            "fecha_desde": args.fecha_desde,
            "dorsal": args.dorsal_inicial + i,
            "activo": True,
        }
        try:
            created = client.post("/planteles/", payload)
            created_rosters.append(created)
        except ApiError as exc:
            roster_errors.append({"index": i + 1, "status": exc.status, "detail": exc.detail, "payload": payload})

    sample_players = [
        {"id": p.get("id"), "nombre": p.get("nombre"), "apellido": p.get("apellido")}
        for p in created_players[:5]
    ]
    sample_rosters = [
        {"id": r.get("id"), "equipo_id": r.get("equipo_id"), "jugador_id": r.get("jugador_id"), "dorsal": r.get("dorsal")}
        for r in created_rosters[:5]
    ]

    print(
        json.dumps(
            {
                "ok": True,
                "equipos_disponibles": len(equipos),
                "jugadores_creados": len(created_players),
                "errores_jugadores": len(player_errors),
                "planteles_creados": len(created_rosters),
                "errores_planteles": len(roster_errors),
                "muestra_jugadores": sample_players,
                "muestra_planteles": sample_rosters,
                "detalle_errores_jugadores": player_errors[:3],
                "detalle_errores_planteles": roster_errors[:3],
            },
            ensure_ascii=True,
        )
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
