# Analisis Exhaustivo Backend por Roles

Fecha de ejecucion: 2026-07-28 06:39:49
Modo: pruebas funcionales sin modificar codigo de aplicacion

## 1) Alcance y metodologia
- Pruebas API ejecutadas contra backend en http://127.0.0.1:8010
- Usuarios evaluados: anonimo, admin, scout, usuario
- Se crearon usuarios temporales para prueba y se eliminaron al finalizar
- Se creo un partido temporal para validar impacto de torneos_clubes y luego se elimino

## 2) Estado general
- Root /: 200
- Docs /docs: 200
- Health DB /health/database: 200
- Contratos RBAC validados: 45/45 correctos
- Contratos con desvio: 0

## 3) Resultados por endpoint y rol
| Rol | Metodo | Endpoint | Esperado | Obtenido | Resultado |
|---|---|---|---:|---:|---|
| anon | GET | /dashboard/summary | 401 | 401 | OK |
| anon | GET | /jugadores/ | 401 | 401 | OK |
| anon | GET | /roles/ | 401 | 401 | OK |
| admin | GET | /dashboard/summary | 200 | 200 | OK |
| scout | GET | /dashboard/summary | 200 | 200 | OK |
| usuario | GET | /dashboard/summary | 200 | 200 | OK |
| admin | GET | /roles/ | 200 | 200 | OK |
| scout | GET | /roles/ | 403 | 403 | OK |
| usuario | GET | /roles/ | 403 | 403 | OK |
| admin | GET | /clubes/ | 200 | 200 | OK |
| scout | GET | /clubes/ | 403 | 403 | OK |
| usuario | GET | /clubes/ | 403 | 403 | OK |
| admin | GET | /maestros/ | 200 | 200 | OK |
| scout | GET | /maestros/ | 403 | 403 | OK |
| usuario | GET | /maestros/ | 403 | 403 | OK |
| admin | GET | /equipos/ | 200 | 200 | OK |
| scout | GET | /equipos/ | 403 | 403 | OK |
| usuario | GET | /equipos/ | 200 | 200 | OK |
| admin | GET | /jugadores/ | 200 | 200 | OK |
| scout | GET | /jugadores/ | 200 | 200 | OK |
| usuario | GET | /jugadores/ | 200 | 200 | OK |
| admin | GET | /torneos/ | 200 | 200 | OK |
| scout | GET | /torneos/ | 200 | 200 | OK |
| usuario | GET | /torneos/ | 200 | 200 | OK |
| admin | GET | /partidos/ | 200 | 200 | OK |
| scout | GET | /partidos/ | 200 | 200 | OK |
| usuario | GET | /partidos/ | 200 | 200 | OK |
| admin | GET | /planteles/ | 200 | 200 | OK |
| scout | GET | /planteles/ | 200 | 200 | OK |
| usuario | GET | /planteles/ | 200 | 200 | OK |
| admin | GET | /scouts/ | 200 | 200 | OK |
| scout | GET | /scouts/ | 200 | 200 | OK |
| usuario | GET | /scouts/ | 403 | 403 | OK |
| admin | GET | /scouting/informes | 200 | 200 | OK |
| scout | GET | /scouting/informes | 200 | 200 | OK |
| usuario | GET | /scouting/informes | 403 | 403 | OK |
| admin | GET | /torneos_clubes/ | 200 | 200 | OK |
| scout | GET | /torneos_clubes/ | 403 | 403 | OK |
| usuario | GET | /torneos_clubes/ | 403 | 403 | OK |
| admin | GET | /usuarios_ligas/ | 200 | 200 | OK |
| scout | GET | /usuarios_ligas/ | 403 | 403 | OK |
| usuario | GET | /usuarios_ligas/ | 403 | 403 | OK |
| admin | GET | /formacion_jugadores/ | 200 | 200 | OK |
| scout | GET | /formacion_jugadores/ | 403 | 403 | OK |
| usuario | GET | /formacion_jugadores/ | 403 | 403 | OK |

## 4) Impacto de parametrizacion torneos_clubes en Partidos
- Se pudo crear partido con torneo_id=c1f90865-96ae-49bc-ab01-4fc0edf21234 y equipos compatibles por temporada/categoria aun cuando membresias torneos_clubes eran local=True, visitante=False.

## 5) Hallazgos enumerados y posible solucion
1. Hallazgo: endpoints protegidos sin token responden 401 (comportamiento correcto por autenticacion faltante).
   Posible solucion: alinear documentación y pruebas para esperar 401 en ausencia de credenciales, y 403 cuando hay token sin permiso.
2. Hallazgo: la matriz RBAC se comporta de forma consistente para admin, scout y usuario en los endpoints validados.
   Posible solucion: mantener una prueba automatizada de contratos por rol para evitar regresiones silenciosas.
3. Hallazgo: `torneos_clubes` no impacta hoy en la validación de creación/edición de partidos.
   Posible solucion: si el negocio lo requiere, validar en backend que `equipo_local_id` y `equipo_visitante_id` pertenezcan al `torneo_id` en `torneos_clubes`.
4. Hallazgo: `formacion_jugadores` depende del partido de forma indirecta (a través de `formaciones`).
   Posible solucion: mantener el diseño actual y reforzar UI/validaciones para seleccionar formación por contexto de partido; evitar cambios de esquema invasivos por ahora.
5. Hallazgo: los datos de prueba temporales se limpiaron correctamente al finalizar la auditoría.
   Posible solucion: conservar esta estrategia de cleanup en cualquier script de validación futura.

## 6) Tablas sin tratamiento
- Tablas de dominio detectadas: 31
- Routers detectados: 25
- Sin tratamiento backend: ninguna tabla sin tratamiento alguno.
- Nota backend: algunas tablas se exponen de forma indirecta (por ejemplo vía `/maestros/*` o `/scouting/*`) y no necesariamente con router dedicado por nombre de tabla.
- Sin tratamiento frontend directo identificado:
   - canchas
   - estadios
   - estados
   - formaciones
   - paises
- Nota frontend: `informes_scouting`, `evaluaciones_jugador`, `videos` y `archivos_adjuntos` sí tienen tratamiento en la pantalla de scouting, aunque no como páginas separadas por tabla.

## 7) Recomendaciones
1. Convertir esta batería en test automatizado de contratos por rol para evitar regresiones silenciosas.
2. Si se desea que torneos_clubes impacte Partidos, agregar validación de pertenencia en create/update de partidos.
3. Consolidar una matriz única de tabla -> API -> UI para reducir desalineaciones de auditoría.
