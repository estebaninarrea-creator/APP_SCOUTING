# Manual de Usuario

Fecha: 2026-07-27
Versión: Scouting App backend + frontend actual

## Portada

**Sistema:** Scouting App

**Documento:** Manual de usuario

**Propósito:** guía paso a paso para operar la aplicación.

## Índice

1. Objetivo
2. Acceso a la aplicación
3. Navegación general
4. Guía rápida de uso
5. Pantallas principales
6. Regla de lectura de pantallas
7. Guía paso a paso por pantalla
8. Recomendaciones de uso
9. Problemas frecuentes
10. Cierre de sesión y buenas prácticas

## 1. Objetivo

Este manual explica cómo usar la aplicación de scouting para administrar datos maestros, jugadores, equipos, torneos, partidos, planteles, scouts y registros de scouting.

La app está pensada para trabajar con usuarios autenticados y permisos por rol. Algunos módulos son de solo lectura para ciertos perfiles.

## 1.1 Guía rápida

Si es la primera vez que usas el sistema, sigue este orden:

1. Entrar con tu usuario y contraseña.
2. Revisar el dashboard.
3. Cargar primero los datos maestros.
4. Crear ligas, clubes y usuarios si corresponde.
5. Registrar jugadores, equipos y torneos.
6. Cargar partidos, planteles y scouting.

## 2. Acceso a la aplicación

1. Abrir la pantalla de login.
2. Ingresar email y contraseña.
3. Presionar `Entrar`.
4. La aplicación lleva al dashboard con el menú lateral y las opciones habilitadas según el rol.

### Roles habituales

- `Admin`: acceso completo a administración y datos maestros.
- `Usuario`: acceso acotado a lectura de algunos módulos operativos.
- `Scout`: acceso a Scouting y módulos asociados según permisos.

## 3. Navegación general

La app utiliza un layout con:

- Barra superior con el nombre de la aplicación.
- Menú lateral para navegar entre módulos.
- Área principal con listados, formularios y filtros.
- Botón de cierre de sesión.

En los listados, la interfaz muestra etiquetas humanas siempre que sea posible. No se recomienda depender de IDs internos.

## 4. Guía rápida de uso

Antes de cargar información operativa, conviene preparar las bases en este orden:

1. Datos Maestros.
2. Ligas.
3. Clubes.
4. Usuarios y Roles.
5. Jugadores.
6. Equipos.
7. Torneos.
8. Partidos.
9. Planteles.
10. Scouts.
11. Scouting.

## 5. Pantallas principales

### Dashboard

Es la pantalla de inicio luego del login.

Qué muestra:

- resumen general del sistema,
- cantidades o indicadores rápidos,
- acceso visual a los módulos más usados.

Qué hacer aquí:

- revisar el estado general,
- entrar a los módulos desde el menú,
- confirmar que el usuario autenticado quedó con el rol correcto.

### Datos Maestros

Sirve para cargar las tablas base del negocio antes de usar los módulos operativos.

Incluye:

- Provincias,
- Ciudades,
- Posiciones,
- Temporadas,
- Categorías,
- Tipos de torneo,
- Criterios de evaluación.

Qué hacer aquí:

- crear catálogos nuevos,
- editar registros existentes,
- eliminar datos de prueba que ya no se usen.

### Ligas

Módulo para administrar ligas deportivas.

Uso habitual:

- alta de ligas,
- edición de datos básicos,
- baja de ligas obsoletas.

### Clubes

Permite administrar los clubes o instituciones.

Uso habitual:

- cargar clubes,
- corregir nombres,
- vincularlos luego con equipos.

### Usuarios

Permite administrar cuentas de acceso al sistema.

Uso habitual:

- crear usuarios,
- asignar rol,
- revisar estado activo,
- actualizar datos personales.

### Roles

Sirve para controlar permisos y accesos.

Uso habitual:

- revisar qué puede ver cada rol,
- validar si un usuario es Admin, Usuario o Scout,
- ajustar permisos cuando se defina un perfil nuevo.

### Jugadores

Módulo para administrar el plantel de jugadores del sistema.

Uso habitual:

- cargar jugadores nuevos,
- editar datos biográficos o deportivos,
- asociar posiciones,
- buscar jugadores existentes.

### Equipos

Permite administrar equipos por club, temporada y categoría.

Uso habitual:

- crear equipos,
- editar información del equipo,
- verificar la temporada y categoría asociadas.

### Torneos

Sirve para administrar torneos y su relación con temporada y categoría.

Uso habitual:

- alta de torneos,
- edición de nombre y clasificación,
- preparación de la competencia antes de cargar partidos.

### Partidos

Módulo para administrar encuentros deportivos.

Uso habitual:

- crear partidos,
- asignar equipos,
- elegir árbitro desde catálogo,
- registrar goles y observaciones,
- gestionar convocados.

### Planteles

Relaciona jugadores con equipos y temporadas.

Uso habitual:

- agregar un jugador al equipo,
- revisar permanencia en la temporada,
- editar fechas o dorsal,
- eliminar relaciones que ya no correspondan.

### Scouts

Administra los perfiles de scouting.

Uso habitual:

- crear scouts,
- vincularlos con usuarios,
- revisar datos de contacto,
- activar o desactivar perfiles.

### Scouting

Concentra informes, evaluaciones, videos y archivos adjuntos.

Uso habitual:

- crear informes de jugadores,
- registrar evaluaciones de partido,
- adjuntar videos,
- adjuntar archivos,
- consultar registros anteriores.

### Arbitros

Catálogo de árbitros disponibles para partidos.

Uso habitual:

- alta y edición de árbitros,
- uso como catálogo para asignación en partidos.

## 6. Regla de lectura de pantallas

Si una pantalla muestra botones deshabilitados o solo lectura, normalmente significa una de estas dos cosas:

- el rol autenticado no tiene permiso de edición,
- el módulo se abrió en modo consulta y no de administración.

En ese caso, el usuario puede revisar los datos pero no modificarlos.

## 7. Guía paso a paso por pantalla

### 3.3.1 Dashboard

Para qué sirve:

- ver el resumen general del sistema.

Qué hacer:

1. Iniciar sesión.
2. Revisar los indicadores principales.
3. Entrar al módulo que necesites desde el menú lateral.

### 3.3.2 Datos Maestros

Para qué sirve:

- cargar y mantener las tablas base de la aplicación.

Qué hacer:

1. Entrar a Datos Maestros.
2. Elegir el bloque que quieras administrar.
3. Presionar `Agregar` si vas a crear un registro nuevo.
4. Completar los campos del formulario.
5. Guardar.
6. Si hace falta, editar o eliminar registros que sean de prueba.

### 3.3.3 Ligas

Para qué sirve:

- definir las ligas que se usarán para temporadas, torneos y equipos.

Qué hacer:

1. Entrar a Ligas.
2. Presionar `Agregar`.
3. Completar el nombre de la liga.
4. Guardar.
5. Usar `Editar` para corregir y `Eliminar` si la liga no se usa.

### 3.3.4 Clubes

Para qué sirve:

- registrar las instituciones deportivas.

Qué hacer:

1. Entrar a Clubes.
2. Crear un club nuevo.
3. Revisar el nombre y datos básicos.
4. Guardar.

### 3.3.5 Usuarios

Para qué sirve:

- administrar las cuentas de acceso.

Qué hacer:

1. Entrar a Usuarios.
2. Crear o editar una cuenta.
3. Asignar el rol correcto.
4. Guardar.
5. Verificar que el usuario pueda entrar con ese rol.

### 3.3.6 Roles

Para qué sirve:

- controlar qué puede ver o hacer cada perfil.

Qué hacer:

1. Entrar a Roles.
2. Revisar la lista disponible.
3. Ajustar permisos si corresponde.
4. Confirmar luego el comportamiento con un usuario real.

### 3.3.7 Jugadores

Para qué sirve:

- cargar y mantener el registro de jugadores.

Qué hacer:

1. Entrar a Jugadores.
2. Presionar `Agregar jugador`.
3. Completar apellido, nombre y demás datos.
4. Agregar posiciones si corresponde.
5. Guardar.
6. Usar el buscador para encontrar jugadores cargados.

### 3.3.8 Equipos

Para qué sirve:

- definir equipos por club, temporada y categoría.

Qué hacer:

1. Entrar a Equipos.
2. Crear un equipo nuevo.
3. Seleccionar club, temporada y categoría.
4. Guardar.

### 3.3.9 Torneos

Para qué sirve:

- registrar los torneos del sistema.

Qué hacer:

1. Entrar a Torneos.
2. Crear un torneo.
3. Seleccionar temporada, categoría y tipo.
4. Guardar.

### 3.3.10 Partidos

Para qué sirve:

- registrar y administrar los partidos.

Qué hacer:

1. Entrar a Partidos.
2. Crear un partido nuevo.
3. Elegir torneo, equipos y árbitro.
4. Completar fecha y observaciones.
5. Guardar.
6. Si hace falta, entrar a convocados y sumar jugadores al partido.

### 3.3.11 Planteles

Para qué sirve:

- relacionar jugadores con equipos y temporadas.

Qué hacer:

1. Entrar a Planteles.
2. Filtrar si hace falta por temporada o equipo.
3. Presionar `Nuevo plantel`.
4. Elegir equipo y jugador.
5. Completar fechas o dorsal si aplica.
6. Guardar.

### 3.3.12 Scouts

Para qué sirve:

- administrar los perfiles de scouting.

Qué hacer:

1. Entrar a Scouts.
2. Crear el perfil del scout.
3. Asociarlo a un usuario de acceso.
4. Guardar.
5. Revisar que el nombre mostrado sea legible.

### 3.3.13 Scouting

Para qué sirve:

- registrar informes, evaluaciones, videos y archivos adjuntos.

Qué hacer:

1. Entrar a Scouting.
2. Elegir la pestaña que corresponda.
3. Presionar `Nuevo registro`.
4. Completar jugador, scout, partido y criterio con los selectores disponibles.
5. Escribir observaciones, valor o datos complementarios.
6. Guardar.
7. Revisar que el registro aparezca en la grilla.

### 3.3.14 Árbitros

Para qué sirve:

- administrar árbitros para poder asignarlos a partidos.

Qué hacer:

1. Entrar a Árbitros.
2. Crear o editar un árbitro.
3. Guardar.
4. Luego usarlo desde la pantalla de Partidos.

### 3.3.15 Criterios de evaluación

Para qué sirve:

- definir qué se va a evaluar en un jugador.

Qué hacer:

1. Entrar a Datos Maestros.
2. Ir al bloque de Criterios de evaluación.
3. Presionar `Agregar`.
4. Escribir nombre y descripción.
5. Guardar.
6. Luego seleccionar ese criterio desde Scouting al crear una evaluación.

## 8. Recomendaciones de uso

1. Cargar primero los catálogos base antes de usar los módulos operativos.
2. Usar nombres claros para que los listados sean fáciles de entender.
3. Revisar el rol antes de pedir cambios si una pantalla aparece en solo lectura.
4. Evitar borrar datos reales sin validar dependencias.

## 9. Problemas frecuentes

### No veo una opción en el menú

Puede ser una restricción del rol o un acceso no habilitado para ese perfil.

### No puedo guardar un registro

Revisar que todos los campos obligatorios estén completos y que existan los catálogos previos.

### Veo IDs o datos raros

Eso suele indicar que falta un catálogo relacionado o que el registro todavía no tiene nombre legible.

## 10. Cierre de sesión y buenas prácticas

1. Cerrar sesión cuando se termine de trabajar.
2. No compartir el usuario y la contraseña.
3. Revisar siempre los datos antes de guardar.
4. Confirmar que el registro quedó visible en la grilla después de crear o editar.

## 4. Orden recomendado de carga de datos

Para trabajar con datos reales, conviene cargar la información en este orden:

1. Datos maestros
2. Ligas y clubes
3. Usuarios y roles
4. Jugadores
5. Equipos
6. Torneos
7. Partidos
8. Planteles
9. Scouts
10. Criterios de evaluación
11. Scouting

### Nota importante

En Scouting, `Criterio` debe existir antes de crear evaluaciones. Si no hay criterios cargados, el formulario de evaluaciones no tiene opciones válidas para ese campo.

## 5. Datos Maestros

Pantalla pensada para administrar tablas base del sistema.

### 5.1 Provincias

Sirven para clasificar ciudades.

Acciones disponibles:

- Agregar
- Editar
- Eliminar

### 5.2 Ciudades

Cada ciudad se asocia a una provincia.

Se recomienda crear primero la provincia y luego la ciudad.

### 5.3 Posiciones

Se usan en jugadores y convocatorias.

Ejemplos:

- Portero
- Defensa
- Centrocampista
- Delantero

### 5.4 Temporadas

Representan el período deportivo de trabajo.

Antes de crear equipos o torneos, la temporada debe estar definida.

### 5.5 Categorías

Se usan para segmentar equipos y torneos.

Ejemplos:

- Primera División
- Sub-20
- Reserva

### 5.6 Tipos de torneo

Clasificación del torneo.

Ejemplos:

- Liga
- Copa
- Amistoso

### 5.7 Criterios de evaluación

Se usan en Scouting para definir qué aspecto se evalúa del jugador.

Ejemplos:

- Velocidad
- Pase
- Técnica
- Definición
- Marca
- Físico

Cada criterio puede tener:

- Nombre
- Descripción
- Estado activo/inactivo

## 6. Ligas, clubes y roles

### Ligas

Se administran desde el módulo correspondiente y sirven como base de temporadas y organización general.

### Clubes

Representan las instituciones deportivas.

### Roles

Se usan para controlar permisos y visibilidad de módulos.

## 7. Usuarios

Los usuarios son las cuentas de acceso al sistema.

Puntos clave:

- Cada usuario tiene un rol.
- El rol determina qué módulos puede ver o modificar.
- Un usuario puede estar asociado a perfiles de negocio como Scout.

## 8. Jugadores

En este módulo se administra el plantel de jugadores del sistema.

Se recomienda completar:

- Apellido y nombre
- Documento o COMET si aplica
- Fecha de nacimiento
- Posición o posiciones
- Datos de contacto o referencia si corresponde

La interfaz usa etiquetas de búsqueda para facilitar selección y evitar capturas manuales con IDs.

## 9. Equipos

Los equipos se organizan por club, temporada y categoría.

Antes de crear un equipo, conviene verificar:

- Club existente
- Temporada válida
- Categoría válida

## 10. Torneos

Los torneos se usan para agrupar partidos y definir competencia.

Antes de crear un torneo, revisar:

- Temporada
- Categoría
- Tipo de torneo

## 11. Partidos

El módulo de Partidos permite administrar encuentros deportivos.

### Datos que suele requerir

- Torneo
- Equipo local
- Equipo visitante
- Fecha del partido
- Cancha
- Árbitro
- Goles y observaciones

### Importante

- El árbitro se selecciona desde un catálogo parametrizado.
- No se deben ingresar IDs a mano si la interfaz ofrece un selector.
- Si el usuario no tiene permiso de edición, verá el módulo en modo lectura.

### Convocados

Dentro del partido se pueden gestionar jugadores convocados.

La interfaz ayuda a:

- ver jugadores disponibles
- filtrar por lado local/visitante
- editar convocados existentes

## 12. Planteles

Planteles relaciona jugadores con equipos y temporadas.

### Uso normal

1. Elegir equipo.
2. Elegir jugador.
3. Definir fechas y dorsal si corresponde.
4. Guardar.

### Reglas comunes

- Un jugador no debe quedar duplicado en la misma temporada si la regla de negocio lo impide.
- Si el backend rechaza la operación, la UI muestra el motivo.

## 13. Scouts

El módulo de Scouts administra perfiles de scouting.

### Qué representa un Scout

- Es un perfil operativo del sistema.
- Puede estar asociado a un usuario de login.
- No debe tratarse como un ID crudo visible para el usuario.

### Datos comunes

- Nombre
- Apellido
- Usuario asociado
- Teléfono
- Email
- Estado activo/inactivo

## 14. Scouting

Este módulo concentra los registros de observación y material asociado.

### Secciones principales

- Informes
- Evaluaciones
- Videos
- Archivos adjuntos

### 14.1 Informes

Relacionan:

- Jugador
- Scout
- Observaciones

### 14.2 Evaluaciones

Relacionan:

- Jugador
- Partido
- Scout
- Criterio de evaluación
- Valor numérico
- Comentario opcional

### 14.3 Videos

Permiten asociar videos a un jugador y, opcionalmente, a un partido.

### 14.4 Archivos adjuntos

Permiten cargar documentos, imágenes u այլ material de apoyo.

### Reglas importantes de uso

- Nunca se deben mostrar IDs internos como dato principal si existe un label humano.
- El selector de `Scout` debe usar los scouts ya creados.
- Si el usuario logueado es un scout, el sistema lo puede preseleccionar por defecto.
- `Partido` y `Criterio` deben seleccionarse desde catálogos existentes.
- `Criterio` debe cargarse primero en Datos Maestros.

## 15. Consejos operativos

- Usar siempre los selectores que ofrece la pantalla.
- No escribir UUIDs manualmente salvo que el sistema lo pida expresamente.
- Confirmar que los datos maestros existen antes de abrir formularios dependientes.
- Si un módulo no deja guardar, revisar primero permisos y luego catálogos asociados.

## 16. Problemas frecuentes

### No aparece un criterio al crear una evaluación

Verificar que exista un alta previa en Datos Maestros > Criterios de evaluación.

### No se puede crear un partido o un plantel

Revisar:

- permisos del rol
- catálogos relacionados
- coherencia de temporada, categoría y equipo

### Veo solo lectura en una pantalla

Eso normalmente significa que el rol autenticado no tiene permiso de edición.

### Un campo muestra un texto genérico en vez del nombre esperado

Normalmente significa que falta completar el catálogo relacionado o que el registro no pudo resolverse en memoria. Conviene revisar el dato maestro correspondiente.

## 17. Recomendación para pasar a datos reales

Antes de cargar información real:

1. Definir el catálogo final de criterios de evaluación.
2. Revisar si las provincias, ciudades, posiciones, ligas y categorías actuales se corresponden con el negocio real.
3. Limpiar registros de prueba que no deban quedar.
4. Confirmar usuarios y roles definitivos.
5. Validar nuevamente con login real.

## 18. Cierre

La aplicación actual ya permite trabajar con el flujo principal de administración y scouting. Para operar con datos reales, lo más importante es completar primero los datos maestros y luego usar esos catálogos desde el resto de los módulos.
