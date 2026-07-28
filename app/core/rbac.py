import json
from collections.abc import Iterable
from pathlib import Path


AVAILABLE_PERMISSIONS = [
    "*",
    "admin:manage",
    "dashboard:view",
    "jugadores:view",
    "jugadores:manage",
    "equipos:view",
    "equipos:manage",
    "planteles:view",
    "planteles:manage",
    "partidos:view",
    "partidos:manage",
    "torneos:view",
    "torneos:manage",
    "partido_jugadores:manage",
    "scouting:view",
    "scouts:view",
]

DEFAULT_ROLE_PERMISSION_MATRIX: dict[str, set[str]] = {
    "admin": {"*"},
    "scout": {
        "dashboard:view",
        "jugadores:view",
        "partidos:view",
        "planteles:view",
        "torneos:view",
        "scouting:view",
        "scouts:view",
    },
    "usuario": {
        "dashboard:view",
        "jugadores:view",
        "equipos:view",
        "planteles:view",
        "partidos:view",
        "torneos:view",
    },
    "invitado": {
        "dashboard:view",
    },
}

RBAC_MATRIX_FILE = Path(__file__).with_name("rbac_matrix.json")


def normalize_role_name(role_name: str | None) -> str:
    return (role_name or "").strip().lower()


def _serialize_matrix(matrix: dict[str, set[str]]) -> dict[str, list[str]]:
    return {role: sorted(permissions) for role, permissions in matrix.items()}


def _load_matrix_from_disk() -> dict[str, set[str]] | None:
    if not RBAC_MATRIX_FILE.exists():
        return None

    with RBAC_MATRIX_FILE.open("r", encoding="utf-8") as handle:
        raw_data = json.load(handle)

    matrix: dict[str, set[str]] = {}
    for role, permissions in raw_data.items():
        normalized_role = normalize_role_name(role)
        if not normalized_role:
            continue

        if not isinstance(permissions, list):
            continue

        matrix[normalized_role] = {permission.strip() for permission in permissions if isinstance(permission, str) and permission.strip()}

    return matrix


def _save_matrix_to_disk(matrix: dict[str, set[str]]) -> None:
    serialized = _serialize_matrix(matrix)
    with RBAC_MATRIX_FILE.open("w", encoding="utf-8") as handle:
        json.dump(serialized, handle, ensure_ascii=False, indent=2)


def _load_or_init_matrix() -> dict[str, set[str]]:
    disk_matrix = _load_matrix_from_disk()
    if disk_matrix is not None and disk_matrix:
        return disk_matrix

    defaults = {role: set(permissions) for role, permissions in DEFAULT_ROLE_PERMISSION_MATRIX.items()}
    _save_matrix_to_disk(defaults)
    return defaults


ROLE_PERMISSION_MATRIX: dict[str, set[str]] = _load_or_init_matrix()


def get_permissions_for_role(role_name: str | None) -> list[str]:
    normalized = normalize_role_name(role_name)
    return sorted(ROLE_PERMISSION_MATRIX.get(normalized, set()))


def get_role_permission_matrix() -> dict[str, list[str]]:
    return _serialize_matrix(ROLE_PERMISSION_MATRIX)


def set_permissions_for_role(role_name: str | None, permissions: Iterable[str]) -> list[str]:
    normalized_role = normalize_role_name(role_name)
    if not normalized_role:
        return []

    normalized_permissions = {permission.strip() for permission in permissions if permission and permission.strip()}
    if "*" in normalized_permissions:
        normalized_permissions = {"*"}

    ROLE_PERMISSION_MATRIX[normalized_role] = normalized_permissions
    _save_matrix_to_disk(ROLE_PERMISSION_MATRIX)
    return sorted(normalized_permissions)


def has_any_permission(role_name: str | None, required_permissions: Iterable[str]) -> bool:
    role_permissions = set(get_permissions_for_role(role_name))
    if "*" in role_permissions:
        return True

    normalized_required = {permission.strip() for permission in required_permissions if permission.strip()}
    if not normalized_required:
        return True

    return any(permission in role_permissions for permission in normalized_required)
