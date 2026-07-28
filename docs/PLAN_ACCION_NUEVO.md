# Plan de accion nuevo (frontend -> backend)

Fecha: 2026-07-26

## Estado actual

- Punto solucionado 1: bloqueo de `/usuarios` por email invalido.
- Resultado: la pantalla `/usuarios` carga correctamente y lista usuarios.
- Ajuste aplicado en datos: `admin@scoutingapp.local` -> `admin@example.com`.
- Ajuste aplicado en seed: usuario default actualizado a `admin@example.com`.
- Punto solucionado 2: cierre de Catalogos (Roles, Ligas, Clubes) con CRUD completo desde frontend.
- Evidencia: en cada modulo se valido crear, editar y eliminar registro temporal, con refresco de tabla y sin errores bloqueantes.
- Punto solucionado 3: cierre de Datos Maestros (Provincias, Ciudades, Posiciones) con CRUD completo desde frontend.
- Evidencia: se validaron altas, ediciones y bajas de registros temporales con mensajes de exito ("Provincia eliminada correctamente", "Ciudad eliminada correctamente", "Posición eliminada correctamente") y conteos finales consistentes.
- Punto solucionado 4: estabilizacion de regresiones backend para continuar Entidades Operativas.
- Evidencia: ajuste de pruebas a endpoints autenticados (Jugadores) y contrato HTTP 409 en Clubes; suite backend en verde (12 passed).
- Punto solucionado 5: cierre de Entidades Operativas (Usuarios, Torneos, Jugadores, Partidos) con matriz frontend ejecutada.
- Evidencia: en cada modulo se valido listar, crear, editar y eliminar registro temporal, con refresco de tabla y sin 500 tras ajustes.
- Ajuste aplicado para cierre de Partidos: mapeo de `local_equipo_id`/`visitante_equipo_id` a `equipo_local_id`/`equipo_visitante_id` en servicio para evitar 500 en alta/edicion.
- Punto solucionado 6: revision integral final (smoke) ejecutada.
- Evidencia: login/logout OK, navegacion principal OK, filtros/paginacion UI OK, mutacion smoke en Partidos (alta+baja) OK, y diagnostico de endpoints sin 500.
- Ajuste aplicado en frontend para cierre del smoke: proteccion de rutas internas con `RequireAuth` en router para evitar acceso post-logout.
- Punto solucionado 7: warning de autenticacion passlib/bcrypt eliminado.
- Evidencia: `bcrypt` fijado a `4.0.1`, login `/auth/login` en 200 y backend sin traza "error reading bcrypt version".

## Objetivo

Cerrar los pendientes funcionales sin romper modulos ya estables, validando cada paso desde frontend y confirmando backend.

## Orden de ejecucion (estricto)

1. Cierre de Catalogos
- Modulos: Roles, Ligas, Clubes.
- Pruebas por modulo: listar, crear, editar, eliminar, refresco de tabla.
- Criterio de salida: CRUD completo en los 3 modulos sin errores 4xx/5xx inesperados.

2. Cierre de Datos Maestros
- Modulos: Provincias, Ciudades, Posiciones.
- Pruebas por modulo: listar, crear, editar, eliminar.
- Casos de negocio: validar mensajes cuando un registro esta en uso.
- Criterio de salida: flujo completo y mensajes claros de error.

3. Cierre de Entidades Operativas
- Modulos: Usuarios, Torneos, Jugadores, Partidos.
- Pruebas por modulo: listar, crear, editar, eliminar.
- Casos invalidos minimos: payload incompleto, referencias inexistentes, duplicados.
- Criterio de salida: errores controlados y UI sin estados inconsistentes.

4. Revision integral final
- Flujos: login/logout, navegacion, filtros, paginacion, mutaciones.
- Verificaciones tecnicas: sin errores de consola bloqueantes, sin 500 en endpoints principales.
- Criterio de salida: smoke completo OK y reporte de cierre.

## Matriz de prueba unica (aplicar a cada modulo)

1. Abrir ruta del modulo.
2. Verificar carga inicial del listado.
3. Crear registro de prueba.
4. Editar registro creado.
5. Eliminar registro creado.
6. Verificar notificacion de exito/error.
7. Verificar consistencia de tabla (conteo y contenido).

## Riesgos y mitigacion

- Riesgo: errores tipo CORS aparentes que oculten fallas backend.
- Mitigacion: revisar backend logs ante cada fallo de red del frontend.

- Riesgo: datos legacy invalidos que rompan response model.
- Mitigacion: saneo de datos antes de validar cierre del modulo.

## Evidencia minima requerida por punto

- Captura de ruta funcional desde frontend.
- Confirmacion de endpoint en backend sin 500.
- Mensaje de estado: "Punto solucionado X" al cerrar cada bloque.
