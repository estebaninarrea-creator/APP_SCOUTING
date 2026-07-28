# Matriz RBAC de Endpoints

Fecha: 2026-07-27

## Grupos de permisos aplicados en backend

Fuente: configuracion en [app/main.py](app/main.py)

- admin:manage
  - /arbitros
  - /canchas
  - /categorias
  - /clubes
  - /criterios_evaluacion
  - /estadios
  - /estados
  - /formacion_jugadores
  - /formaciones
  - /ligas
  - /maestros
  - /roles
  - /temporadas
  - /tipos_torneo
  - /torneos_clubes
  - /usuarios
  - /usuarios_ligas

- dashboard:view
  - /dashboard/summary

- jugadores:view
  - /jugadores

- equipos:view
  - /equipos

- planteles:view
  - /planteles

- partidos:view
  - /partidos
  - /partidos/{partido_id}/jugadores

- torneos:view
  - /torneos

- scouting:view
  - /scouting

- scouts:view
  - /scouts

- Publico real (sin auth)
  - /auth/login
  - /auth/signup
  - /health/database
  - /

- Requiere token (auth)
  - /auth/me

## Contrato de estado por seguridad

1. Sin token en endpoint protegido: 401.
2. Con token y rol sin permiso: 403.
3. Con token y rol autorizado: 200 (o 201/204 en mutaciones).

## Endpoints criticos para no-regresion

- /dashboard/summary
- /jugadores/
- /roles/
- /clubes/
- /maestros/
- /scouting/informes
- /scouts/
- /torneos_clubes/
- /usuarios_ligas/
- /formacion_jugadores/

## Estrategia de test recomendada

1. Contrato 401: endpoint protegido sin token debe retornar 401.
2. Contrato 403: endpoint protegido con usuario sin permiso debe retornar 403.
3. Contrato 200/201: endpoint con rol autorizado debe retornar exito.
4. Para contratos de permisos, preferir TestClient con dependency_overrides en tests aislados.
5. Ejecutar bateria P0: `python -m pytest tests/test_rbac_phase_p0_matrix.py -q`.
6. Ejecutar no-regresion general: `python -m pytest -m no_regression -q`.

## Cobertura automatizada P0

- Archivo: `tests/test_rbac_phase_p0_matrix.py`
- Valida:
  - anonimo (401) en endpoints protegidos
  - admin/scout/usuario por endpoint critico
  - endpoints publicos base
