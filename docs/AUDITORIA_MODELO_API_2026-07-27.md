# Auditoria de Tablas del Modelo y Cobertura API

Fecha: 2026-07-27
Alcance: todas las tablas detectadas en app/models (excepto base, __init__, models_generados), routers backend y consumo desde frontend.

## 1) Inventario general

Tablas de dominio detectadas: 32
Routers activos: 21
Endpoints declarados: 132

## 2) Matriz tabla vs implementacion

Leyenda de estado:
- Completo: tabla con API utilizable y consumo real en frontend
- Backend completo sin UI: API implementada, sin consumo de interfaz actual
- Parcial: existe uso indirecto o referencia, pero sin modulo CRUD/catalogo completo
- Pendiente: tabla sin API de negocio explicita

| Tabla | API backend | Uso frontend | Estado | Criticidad |
|---|---|---|---|---|
| arbitros | Si (router arbitros) | No | Backend completo sin UI | Media |
| archivos_adjuntos | Si (scouting/archivos) | No | Backend completo sin UI | Media |
| canchas | No CRUD propio | Solo campo cancha_id en partidos | Parcial | Alta |
| categorias | Si | Si | Completo | Baja |
| ciudades | Si (maestros) | Si | Completo | Baja |
| clubes | Si | Si | Completo | Baja |
| criterios_evaluacion | No CRUD propio | No | Pendiente (referenciado por evaluaciones) | Alta |
| equipos | Si | Si | Completo | Baja |
| estadios | No CRUD propio | No | Parcial (validaciones y relaciones) | Alta |
| estados | Si | No | Backend completo sin UI | Baja |
| evaluaciones_jugador | Si (scouting/evaluaciones) | No | Backend completo sin UI | Media |
| formaciones | Si | No | Backend completo sin UI | Media |
| formacion_jugadores | No CRUD propio | No | Pendiente | Media |
| informes_scouting | Si (scouting/informes) | No | Backend completo sin UI | Media |
| jugadores | Si | Si | Completo | Baja |
| jugadores_posiciones | Si (via payload jugador) | Si | Completo | Baja |
| ligas | Si | Si | Completo | Baja |
| paises | Si (maestros/paises) | No directo | Backend completo sin UI | Baja |
| partidos | Si | Si | Completo | Baja |
| partido_jugadores | Si | Si | Completo | Baja |
| planteles | Si | Si | Completo | Baja |
| posiciones | Si (maestros/posiciones) | Si | Completo | Baja |
| provincias | Si (maestros/provincias) | Si | Completo | Baja |
| roles | Si | Si | Completo | Baja |
| scouts | Si | No | Backend completo sin UI | Media |
| temporadas | Si | Si (uso directo en paginas) | Completo | Baja |
| tipos_torneo | Si | Si (uso directo en paginas) | Completo | Baja |
| torneos | Si | Si | Completo | Baja |
| torneos_clubes | No CRUD propio | No | Pendiente | Media |
| usuarios | Si | Si | Completo | Baja |
| usuarios_ligas | No CRUD propio | No | Pendiente | Media |
| videos | Si (scouting/videos) | No | Backend completo sin UI | Media |

## 3) Hallazgos principales

### 3.1 Brecha alta en catalogos/relaciones clave de competencia
Tablas afectadas:
- canchas
- estadios
- criterios_evaluacion

Riesgo:
- Se usan referencias en otros modulos, pero sin gestion operativa completa en API/UI.
- Puede forzar carga manual en BD o scripts para operar escenarios reales.

Estimacion correccion:
- 16 a 28 horas

### 3.2 Bloques backend listos pero sin interfaz
Modulos con API y sin consumo UI actual:
- arbitros
- scouting (informes, evaluaciones, videos, archivos)
- scouts
- formaciones
- estados
- paises

Riesgo:
- Inversion backend sin valor visible para usuario final hasta cerrar frontend.

Estimacion correccion:
- 40 a 72 horas (segun alcance UX)

### 3.3 Tablas relacionales sin superficie funcional
Tablas:
- formacion_jugadores
- torneos_clubes
- usuarios_ligas

Riesgo:
- Relaciones criticas quedan implícitas o incompletas para negocio multi-entidad.
- Dificulta trazabilidad y administracion por usuarios no tecnicos.

Estimacion correccion:
- 18 a 32 horas

## 4) Plan de solucion por importancia y criticidad

## P0 - Diferido por ahora
1. Implementar API CRUD/catalogos para estadios y canchas.
2. Implementar API para criterios_evaluacion y validaciones de integridad en evaluaciones.
3. Agregar pruebas de integracion para estos 3 bloques con RBAC.

Salida esperada:
- Partidos y scouting operables sin depender de carga manual SQL.
- Este bloque no se considera prioritario para la app en este momento.

## P1 - Valor funcional alto (cerrar backend ya existente en UI)
1. Exponer en frontend modulos arbitros, scouts y scouting.
2. Crear paginas de consulta/alta/edicion para informes, evaluaciones, videos, adjuntos.
3. Agregar navegacion y permisos por perfil.

Salida esperada:
- Funcionalidad de scouting utilizable extremo a extremo.

## P2 - Gobernanza de relaciones
1. Implementado en frontend como modulo administrativo para torneos_clubes, usuarios_ligas y formacion_jugadores.
2. Queda como punto de diseño futuro definir si formacion_jugadores debe mantenerse directa o derivarse desde formaciones.
3. La auditoria minima de cambios (created_by, updated_by si aplica) sigue como mejora pendiente de modelado.

Salida esperada:
- Relaciones administrables desde UI y base tecnica lista para evolucionar trazabilidad.

## 5) Estimacion global sugerida

- P0: 16 a 28 horas
- P1: 40 a 72 horas
- P2: 18 a 32 horas
- Total orientativo: 74 a 132 horas

## 6) Recomendaciones de ejecucion

1. Priorizar P0 antes de ampliar nuevas features.
2. En paralelo, alinear suites de pruebas con RBAC para evitar falsos negativos.
3. Ejecutar entregas incrementales por modulo (API + UI + tests) para reducir riesgo de regresion.
