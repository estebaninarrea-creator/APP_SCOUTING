# Plan de Accion Integral

Fecha: 2026-07-28
Base: resultados de auditoria funcional por roles y cobertura backend/frontend.

## 1) Objetivo

- Consolidar seguridad y contratos de acceso por rol.
- Cerrar brechas funcionales de frontend aun no expuestas.
- Definir reglas de negocio pendientes sin romper flujos estables.
- Mantener limpieza de datos de prueba y trazabilidad operativa.

## 2) Prioridades

- P0 (inmediato): contratos de seguridad y regresion.
- P1 (corto plazo): cobertura frontend directa de tablas faltantes.
- P2 (decisiones de negocio): impacto de torneos_clubes en partidos y criterio final de formacion_jugadores.
- P3 (calidad continua): observabilidad, limpieza y documentacion viva.

## 3) Plan por fases

### Fase P0 - Seguridad y Contratos (1 a 2 dias)

Estado: iniciado (2026-07-28)

Avance aplicado:
- Suite automatizada de contratos por rol creada y ejecutada en verde.
- Matriz RBAC documental ajustada a contrato real 401/403.
- Endpoints criticos de no-regresion definidos.
- Flujo unificado de no-regresion habilitado por marcador pytest: `python -m pytest -m no_regression -q`.
- Warning de TestClient resuelto agregando dependencia `httpx2`.
- CI backend agregado: smoke en push/PR y full suite en ejecucion manual/programada.

1. Estandarizar contrato de respuestas:
   - Sin token: 401.
   - Con token sin permiso: 403.
2. Convertir la bateria de auditoria por roles en pruebas automatizadas de contrato.
3. Publicar matriz endpoint -> permiso -> respuesta esperada en un documento unico.
4. Agregar chequeo de no-regresion en CI para endpoints criticos:
   - dashboard
   - jugadores
   - planteles
   - scouting
   - relaciones administrativas

Criterio de salida P0:
- Todas las pruebas de contrato verdes.
- Evidencia de ejecucion en reporte automatico.

### Fase P1 - Cobertura Frontend Directa (4 a 7 dias)

Tablas con backend operativo pero sin tratamiento frontend directo actual:
- canchas
- estadios
- estados
- formaciones
- paises

Ejecucion recomendada por modulo (uno por vez):
1. Listado y filtros.
2. Alta y edicion.
3. Baja con validacion de dependencias.
4. Control RBAC de vista y gestion.
5. Prueba manual de humo y prueba automatizada minima.

Orden sugerido:
1. estados
2. paises
3. estadios
4. canchas
5. formaciones

Criterio de salida P1:
- CRUD funcional o gestion equivalente en cada modulo.
- Sin errores 500 en flujos principales.
- Contratos RBAC cubiertos para cada nuevo acceso.

### Fase P2 - Reglas de Negocio Pendientes (2 a 4 dias)

1. Definir si torneos_clubes debe condicionar la configuracion de partidos.
   - Opcion A: solo catalogo administrativo (sin bloqueo).
   - Opcion B: regla obligatoria (equipos del partido deben pertenecer al torneo en torneos_clubes).
2. Si se aprueba Opcion B, implementar validacion backend en alta/edicion de partidos y mensajes claros en frontend.
3. Formalizar criterio de uso de formacion_jugadores:
   - Gestion directa desde modulo de relaciones.
   - O gestion derivada desde flujo de formaciones por partido.

Criterio de salida P2:
- Decision funcional documentada y aplicada.
- Casos de prueba del negocio actualizados.

### Fase P3 - Calidad Continua y Operacion (1 a 2 dias)

1. Estandarizar limpieza de datos temporales en scripts de validacion.
2. Crear plantilla unica de reporte de pruebas (backend + frontend + roles).
3. Incorporar checklist de salida por release:
   - build frontend
   - pruebas backend
   - smoke autenticado
   - limpieza de datos QA

Criterio de salida P3:
- Pipeline y reportes repetibles sin intervencion manual extensiva.

## 4) Matriz de riesgos y mitigacion

1. Riesgo: romper flujos estables al abrir nuevas pantallas.
   - Mitigacion: habilitar por modulo, pruebas por feature y rollback rapido.
2. Riesgo: desalineacion entre reglas de negocio y codigo.
   - Mitigacion: decision funcional previa en P2 antes de cambios de validacion.
3. Riesgo: falsos positivos en pruebas por datos sucios.
   - Mitigacion: fixtures aisladas y limpieza obligatoria post-prueba.

## 5) Entregables

1. Matriz RBAC consolidada y versionada.
2. Suite automatizada de contratos por rol.
3. Modulos frontend pendientes cerrados (P1).
4. Decision e implementacion de regla torneos_clubes sobre partidos (si aplica).
5. Reporte final de cierre con evidencia.

## 6) Definicion de completado

- Seguridad: contratos 401/403/200 validados por rol.
- Funcionalidad: tablas pendientes con tratamiento frontend directo.
- Negocio: reglas pendientes resueltas y documentadas.
- Operacion: limpieza de datos QA y reporte repetible.
