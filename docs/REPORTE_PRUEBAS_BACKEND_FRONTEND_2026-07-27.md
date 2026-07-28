# Reporte de Pruebas Backend y Frontend

Fecha: 2026-07-27
Alcance: Validacion funcional y tecnica de backend FastAPI + frontend React
Condicion solicitada: sin modificar codigo

Actualizacion de estado (post-correcciones):
- P0 aplicado: autenticacion de tests y smoke corregida.
- P1 aplicado: matriz RBAC documentada + tests de contrato 401/403.
- P2 aplicado: code splitting por rutas en frontend.
- P2 adicional aplicado: carga diferida de catalogos en modales pesados (Partidos/Jugadores).
- UI referencial aplicada: selector de árbitros en Partido, etiqueta humana de usuario en Scouts y matchcode de jugadores en Scouting.
- Fix funcional aplicado: creación de planteles validada en UI y backend con contrato RBAC.

## 1) Resumen ejecutivo

Estado general: aplicacion operativa con credenciales validas y suite automatizada alineada con RBAC.

Resultado consolidado:
- Backend en ejecucion: OK
- Frontend build produccion: OK
- Pruebas automatizadas backend: OK (17 passed)
- Prueba smoke frontend: OK (autenticada)
- Flujo UI convocados (partidos): OK en validacion manual reciente
- Dashboard: OK con cantidades para usuario con permisos limitados
- Partido: OK con selección de árbitro parametrizado desde catálogo
- Scouts: OK mostrando usuario asociado sin UUID crudo
- Scouting: OK con jugador seleccionable por matchcode
- Planteles: OK creando registros desde UI y API con permisos de admin
- Planteles: OK mostrando el motivo de rechazo cuando un alta entra en conflicto
- UI por roles validada: Usuario accede a Planteles en lectura y queda bloqueado en Scouting; Scout accede a Scouting.

## 2) Evidencia de ejecucion

### 2.1 Backend - pytest global
Comando:
- python -m pytest -q

Resultado:
- Falla en fase de coleccion, sin ejecutar tests.
- Causa: archivo legacy fuera de carpeta tests ejecuta llamadas HTTP y termina con SystemExit(1) al recibir 401.

Observacion:
- test_frontend_connection.py no se comporta como test aislado de pytest y rompe la corrida global.

### 2.2 Backend - pytest sobre carpeta tests
Comando:
- python -m pytest tests -q

Resultado:
- 17 tests detectados
- 17 pasaron

Novedad:
- Se agrego suite de contrato RBAC (401 sin token y 403 sin permiso) para evitar regresiones de seguridad.
- Se agrego contrato de planteles para crear/eliminar con admin y bloquear creación sin permiso.

### 2.3 Frontend - build
Comando:
- npm run build

Resultado:
- Build exitoso
- Sin advertencias de chunk > 500 kB
- index-gLISLJUf.js: 332.64 kB (gzip 106.40 kB)
- PartidosPage-Bfc8xIR9.js: 20.14 kB
- JugadoresPage-C6qHHw9M.js: 7.38 kB
- ScoutingPage-uT5j0yp6.js: 29.36 kB

Impacto:
- Mejora de performance inicial sostenida por particion de rutas y diferimiento de catalogos en formularios.

### 2.4 Frontend - smoke test
Comando:
- npm run test:smoke

Resultado:
- OK
- El smoke ahora exige token/login de test y valida endpoints protegidos correctamente.

### 2.7 Hallazgo D - avance de performance
Comando:
- npm run build

Resultado:
- Se aplico code splitting por rutas (lazy loading).
- El bundle principal bajo a ~332.64 kB (antes ~850 kB).
- Se eliminaron warnings de chunk > 500 kB.
- Se diferio carga de catalogos hasta apertura de modal en Partidos y Jugadores.

### 2.5 Verificacion runtime autenticada
Smoke de endpoints con Authorization Bearer:
- GET /health/database: 200
- GET /ligas/: 200
- GET /clubes/: 200
- GET /jugadores/: 200
- GET /partidos/: 200
- GET /maestros/: 200

Conclusion:
- El backend responde correctamente cuando el cliente cumple autenticacion/autorizacion.

### 2.6 Verificacion funcional UI (partidos/convocados)
Estado observado:
- Editar convocado muestra alerta, fila resaltada y chip En edicion
- Al seleccionar jugador con multiples posiciones, Posicion cambia a Select y preselecciona principal
- Opciones de posicion visibles correctamente

### 2.7 Verificacion UI complementaria
Estado observado:
- En Partidos el formulario permite elegir árbitro parametrizado.
- En Scouts el selector muestra el usuario asociado con una etiqueta legible.
- En Scouting los registros nuevos usan selector de jugador con matchcode derivado de datos existentes.
- En Planteles el formulario ahora expone el error de backend si una creación no es válida.

## 3) Hallazgos con criticidad y estimacion

### Hallazgo A - Suite automatizada desalineada con RBAC
Criticidad: Alta
Impacto:
- Falsos negativos en CI/local
- Baja confianza en regresiones
Causa:
- Tests llaman endpoints protegidos sin token ni override de dependencia
Estado: Resuelto
Acciones aplicadas:
- Fixture de autenticacion reusable en tests.
- Migracion de tests de integracion a TestClient autenticado.
- Smoke frontend autenticado.

### Hallazgo B - Archivo legacy rompe pytest global
Criticidad: Media
Impacto:
- pytest -q deja de ser util para ver estado real del proyecto
Causa:
- script con side effects en raiz nombrado con patron de test
Estado: Resuelto
Acciones aplicadas:
- El script legacy ya no ejecuta side effects al importarse.

### Hallazgo C - Smoke frontend no contempla auth
Criticidad: Media
Impacto:
- Reporta falla aunque sistema este sano para usuarios autenticados
Causa:
- requests sin token a endpoints protegidos
Estado: Resuelto
Acciones aplicadas:
- Token/login de smoke incorporado.

### Hallazgo D - Bundle principal elevado
Criticidad: Baja
Impacto:
- Penaliza tiempo de carga inicial
Causa:
- chunk unico grande en build
Estado: Resuelto
Acciones aplicadas:
- Code splitting por rutas pesadas.
- Carga diferida de modales/catalogos voluminosos en Partidos/Jugadores.

### Hallazgo E - Referencias humanas ausentes en formularios
Criticidad: Media
Impacto:
- Dificulta seleccionar entidades existentes y aumenta errores de captura manual
Causa:
- Formularios basados en IDs crudos sin etiquetas de contexto
Estado: Resuelto
Acciones aplicadas:
- Árbitro parametrizado en Partido.
- Usuario asociado visible en Scouts.
- Matchcode de jugadores en Scouting.

### Hallazgo F - Alta de plantel bloqueada por fixture de auth desacoplada
Criticidad: Alta
Impacto:
- Imposible validar la creación de planteles desde la suite y el flujo real quedaba sin cobertura útil
Causa:
- La fixture de autenticación de tests devolvía un usuario SQLAlchemy detached y rompía `require_permissions`
Estado: Resuelto
Acciones aplicadas:
- Fixture de auth de tests reemplazada por stub estable con rol materializado.
- Contrato de planteles agregado para admin y usuario sin permiso.

## 4) Plan recomendado por prioridad

P0 (estado: completado)
- Normalizar autenticacion en tests backend y frontend smoke
- Asegurar que pytest global sea ejecutable sin errores de coleccion

P1 (estado: completado)
- Matriz oficial endpoint -> permiso -> estrategia de test documentada.
- Tests de contrato para respuestas 401/403 implementados.

P2 (estado: completado)
- Mejoras de performance frontend (chunking) aplicadas en rutas.
- Lazy interno en catalogos pesados aplicado en modales de Partidos/Jugadores.
- Referencias humanas aplicadas en formularios de Partidos, Scouts y Scouting.
- Planteles cubierto con contrato de admin/usuario y flujo UI validado.

## 5) Conclusiones

- La aplicacion funciona en ejecucion real con usuario autenticado, incluyendo dashboard con cantidades.
- La calidad de pruebas ya quedo alineada con RBAC y con contratos de seguridad basicos.
- La optimizacion de carga inicial quedo consolidada con chunking por rutas y carga diferida en modales pesados.
- La validacion final por roles confirmo la segmentacion esperada entre Usuario y Scout en la UI.
