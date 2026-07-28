# Guia Operativa: Estadio y Cancha

## Objetivo

Evitar datos duplicados y dejar claro que Cancha es un catalogo y que la relacion se define desde Estadio.

## Regla de carga

1. Crear/editar Cancha en Datos Maestros con nombre y descripcion.
2. Crear/editar Estadio con datos de infraestructura.
3. Seleccionar la cancha desde Estadio mediante `cancha_id`.

## Que va en Estadio

- Nombre del estadio.
- Club.
- Ciudad.
- Capacidad.
- Medidas del campo (ancho y largo).

## Que va en Cancha (catalogo)

- Nombre (ejemplo: Cesped sintetico).
- Descripcion (ejemplo: Superficie sintetica de ultima generacion).

## Relacion con otras tablas

- El estadio sigue siendo la referencia principal.
- El estadio guarda `cancha_id`.
- Cancha no guarda `estadio_id`.