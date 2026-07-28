# Manual Técnico

Fecha: 2026-07-27
Versión: Scouting App backend + frontend actual

## Portada

**Sistema:** Scouting App

**Documento:** Manual técnico

**Propósito:** soporte, desarrollo, mantenimiento y análisis funcional.

## Índice

1. Objetivo
2. Arquitectura general
3. Estructura del backend
4. Estructura del frontend
5. Autenticación y permisos
6. Datos y catálogos críticos
7. Dependencias de negocio
8. Build y ejecución local
9. Validaciones y pruebas
10. Troubleshooting
11. Mantenimiento recomendado
12. Referencias de soporte

## 1. Objetivo

Este documento resume la arquitectura, módulos, permisos, ejecución local y criterios técnicos de operación de la aplicación.

Está orientado a soporte, desarrollo, análisis funcional y mantenimiento.

## 2. Arquitectura general

La solución está compuesta por:

- Backend: FastAPI + SQLAlchemy + Pydantic.
- Frontend: React + TypeScript + Vite + Material UI + TanStack Query.
- Base de datos: PostgreSQL.
- Autenticación: JWT con permisos por rol.

## 3. Estructura del backend

### 3.1 Capas principales

- `app/models`: modelos ORM.
- `app/schemas`: contratos Pydantic de entrada y salida.
- `app/services`: lógica de negocio y CRUD.
- `app/routers`: endpoints HTTP.
- `app/core`: seguridad, RBAC y utilidades compartidas.
- `app/dependencies.py`: sesión de BD y usuario autenticado.

### 3.2 Módulos funcionales expuestos

- Auth: login, signup y me.
- Usuarios, Roles y Usuarios-Ligas.
- Ligas, Clubes, Equipos, Torneos.
- Jugadores, Planteles, Partido-Jugadores.
- Partidos, Árbitros, Canchas, Estadios, Estados.
- Maestros: provincias, ciudades, posiciones, temporadas, categorías, tipos de torneo.
- Scouts.
- Scouting: informes, evaluaciones, videos, archivos adjuntos.

## 4. Estructura del frontend

### 4.1 Organización funcional

- `src/pages`: pantallas por módulo.
- `src/api/services`: clientes por recurso.
- `src/types`: tipos compartidos.
- `src/components`: componentes reutilizables.
- `src/config`: RBAC y configuración de entorno.

### 4.2 Patrones de UI

- Carga de datos con TanStack Query.
- Formularios y diálogos en Material UI.
- Listados en tablas reutilizables.
- Selectores humanos en vez de IDs crudos cuando existe catálogo disponible.

## 5. Autenticación y permisos

### 5.1 Login

El backend emite JWT en `/auth/login`.

La respuesta de login incluye:

- `access_token`
- `usuario_id`
- `rol_id`
- `rol_nombre`
- `permissions`

### 5.2 RBAC

Los permisos se resuelven por rol y se validan en backend.

Ejemplos de permisos:

- `admin:manage`
- `jugadores:view`
- `partidos:view`
- `planteles:view`
- `scouting:view`
- `scouts:view`

### 5.3 Consideraciones técnicas

- No asumir que el frontend puede operar solo con permisos visibles.
- El backend sigue siendo la fuente de verdad.
- La sesión del frontend usa `localStorage` para token y permisos derivados.

## 6. Datos y catálogos críticos

### 6.1 Maestros

Se recomienda mantener correctamente cargados:

- provincias
- ciudades
- posiciones
- temporadas
- categorías
- tipos de torneo
- criterios de evaluación

### 6.2 Catálogos operativos

- árbitros para partidos
- equipos para partidos y planteles
- jugadores para scouting
- scouts para informes y evaluaciones

## 7. Dependencias de negocio

### 7.1 Partidos

Partidos depende de:

- torneos,
- equipos,
- árbitros,
- canchas/estadios según el caso.

### 7.2 Planteles

Planteles depende de:

- jugadores,
- equipos,
- temporadas,
- reglas de unicidad por temporada.

### 7.3 Scouting

Scouting depende de:

- jugadores,
- partidos,
- scouts,
- criterios de evaluación.

## 8. Build y ejecución local

### 8.1 Backend

Comandos habituales:

- iniciar servidor: `uvicorn app.main:app --host 127.0.0.1 --port 8010`
- pruebas: `python -m pytest tests -q`

### 8.2 Frontend

Comandos habituales:

- desarrollo: `npm run dev`
- build: `npm run build`

## 9. Validaciones y pruebas

Pruebas ya consolidadas en esta versión:

- backend green con suite en carpeta `tests`.
- build frontend exitosa.
- validación UI con roles reales.
- contratos de RBAC para 401/403.

## 10. Troubleshooting

### 10.1 Error de red en login

Revisar que el backend esté corriendo en `127.0.0.1:8010`.

### 10.2 Pantalla en solo lectura

Normalmente significa falta de permiso de edición o rol restringido.

### 10.3 IDs visibles en UI

Si aparece un UUID, revisar si falta catálogo para traducirlo a nombre legible.

### 10.4 Fallo al crear evaluaciones

Verificar que existan:

- partido válido,
- scout válido,
- criterio de evaluación válido,
- jugador válido.

## 11. Mantenimiento recomendado

1. Mantener alineados backend y frontend para RBAC.
2. Registrar catálogos base antes de cargar datos reales.
3. Evitar fixtures con ORM detached en pruebas.
4. Revisar que los documentos de pruebas y manuales se actualicen junto con el código.

## 12. Referencias de soporte

- [Reporte de pruebas](REPORTE_PRUEBAS_BACKEND_FRONTEND_2026-07-27.md)
- [Auditoría de modelo y API](AUDITORIA_MODELO_API_2026-07-27.md)
- [Plan de acción](PLAN_ACCION_NUEVO.md)