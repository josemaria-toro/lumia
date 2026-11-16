# Design

## Context

Véase `proposal.md` para la motivación y las especificaciones de esta propuesta para los contratos funcionales. El repositorio no contiene código de producto; las reglas del harness (`harness/rules/`) establecen arquitectura hexagonal, SOLID, inyección de dependencias por constructor y Options para configuración. También fijan C# o Python para backend, React para frontend, PostgreSQL para persistencia, Docker para contenerización y pruebas/calidad obligatorias.

## Goals / Non-Goals

**Goals:**

- Establecer una arquitectura compatible con las reglas del harness y que permita probar de forma aislada las capacidades descritas.
- Separar las integraciones externas y los procesos programados de la interfaz y de las reglas de negocio.
- Definir límites de seguridad, persistencia, configuración y validación que rijan la implementación.

**Non-Goals:**

- Elegir un proveedor comercial SMTP distinto del protocolo configurable o proveedores de metadatos adicionales a IMDb y TMDB.
- Definir detalles de despliegue de producción, capacidad de infraestructura o disponibilidad que no estén descritos en los requisitos.
- Diseñar funcionalidades de descarga de medios sin conexión; los favoritos solo se marcan y gestionan.

## Decisions

### Backend C#/.NET y frontend React con TypeScript

El backend se implementará en C#/.NET, según la elección del usuario, y la interfaz web en React con TypeScript, de acuerdo con las tecnologías de frontend del harness. Los proyectos se organizarán en `backend/` y `frontend/`. Las rutas de API seguirán `/api/v<num-version>/<path>`. Cualquier framework o dependencia no incluido en `harness/rules/technologies.md` requerirá un ADR antes de su adopción.

**Alternativas consideradas:** Python está permitido para backend, pero se eligió C#/.NET; no se propone otro framework de frontend.

### Arquitectura hexagonal con límites de entrega, aplicación, dominio e infraestructura

Las reglas de negocio y casos de uso no dependerán de PostgreSQL, proveedores externos ni componentes de interfaz. Los puertos de aplicación separarán persistencia, correo, fuentes de metadatos, IPTV, acceso al sistema de archivos y reproducción; los adaptadores realizarán esas integraciones. Las dependencias se inyectarán por constructor y toda configuración se expondrá mediante Options (véase «Configuración por capas»).

**Alternativas consideradas:** una arquitectura monolítica en capas acopladas a sus proveedores simplificaría el inicio, pero dificultaría sustituir integraciones y probar reglas de negocio independientemente.

### Configuración por capas: JSON, entorno, ficheros de secretos y base de datos

Los servicios (API y trabajador) compondrán su configuración con cuatro proveedores y los expondrán mediante Options: ficheros JSON (valores por defecto), variables de entorno, ficheros de secretos y un proveedor propio basado en base de datos. La cadena de conexión y la clave de cifrado de valores sensibles se leen solo de ficheros de secretos (pueden ser ficheros distintos, con permisos restringidos y fuera del repositorio), porque son necesarias para llegar a la base de datos y descifrar sus valores; el resto de la configuración, incluidas las feature flags, rutas y países de ingestión, parámetros SMTP y plataformas de metadatos, reside en la base de datos. En caso de colisión de claves prevalece la base de datos, después el entorno y por último JSON; los ficheros de secretos aportan únicamente la cadena de conexión y la clave de cifrado, por lo que no colisionan con los demás.

El arranque sigue dos fases: primero se construye la configuración de JSON, entorno y ficheros de secretos para obtener la cadena de conexión y la clave de cifrado; después, el proveedor de base de datos lee la configuración una única vez, antes de registrar los servicios y de atender peticiones o ejecutar tareas. Si esa carga falla, el servicio no arranca (fallo rápido). Los cambios en base de datos se aplican en el siguiente reinicio; no hay recarga en caliente. Los valores sensibles se guardan cifrados (columna marcada como sensible) con una clave que llega solo desde un fichero de secretos, y no se registran ni se devuelven en claro.

La tabla de configuración seguirá `snake_case`, con `created_at` y `updated_at` obligatorios y `created_by` y `updated_by` opcionales, y se incluirá en el script SQL fechado. El proveedor será un adaptador de infraestructura sin dependencias del dominio. Los ficheros ini y xml no estarán soportados en esta plataforma y el uso de un gestor de secretos externo queda fuera de este alcance; la exclusión de ini/xml respecto a la regla de configuración del harness se documentará mediante ADR del proyecto.

**Alternativas consideradas:** mantener las credenciales de integraciones en ficheros de secretos aislaría los secretos de la base de datos, pero se descartó para centralizar toda la configuración; guardarlas en claro contradice la regla de seguridad de secretos. Recargar la configuración en caliente permitiría cambios inmediatos, pero se descartó por simplicidad y previsibilidad.

### Aplicación web y API

La aplicación React consumirá una API versionada. La API validará las entradas en sus límites, comprobará autorización por operación y recurso y limitará CORS a los orígenes necesarios. La autenticación utilizará las cookies de sesión definidas en `user-sessions`; las operaciones que modifican estado deberán protegerse frente a solicitudes no autorizadas originadas en otros sitios.

**Alternativas consideradas:** autenticar cada petición con credenciales en el cliente no coincide con el requisito de sesión basada en cookies.

### Persistencia PostgreSQL con contratos explícitos de datos

PostgreSQL será la base de datos. Se utilizará Entity Framework, incluido en las tecnologías admitidas, si no se justifica otra alternativa mediante ADR. Las tablas y columnas seguirán `snake_case` e incluirán `created_at`, `updated_at` obligatorios y `created_by`, `updated_by` opcionales. Los cambios de esquema se entregarán mediante scripts SQL `yymmdd.sql`, sin migraciones automáticas; cada script incluirá la creación de la base de datos Lumia y los tres usuarios de base de datos requeridos por el harness.

Las cuentas de aplicación y mantenimiento tendrán privilegios separados. Las operaciones de borrado diferido deberán satisfacer el plazo de eliminación especificado y evitar conservar datos personales fuera de ese alcance.

**Alternativas consideradas:** otro motor de base de datos no está admitido por el harness; las migraciones de esquema están expresamente prohibidas.

### Procesamiento de tareas programadas mediante un trabajador aislado

El escaneo de archivos, la actualización IPTV, la gestión de vencimientos y otras tareas periódicas se ejecutarán fuera del ciclo de petición interactivo. El trabajador registrará un estado consultable por la administración y será reiniciable sin perder la planificación persistida. No se introduce un broker de mensajes inicialmente; si la fiabilidad o distribución requiere mensajería, se usará RabbitMQ y se documentará la decisión mediante ADR.

**Alternativas consideradas:** ejecutar las tareas dentro de peticiones web perjudicaría su duración y recuperación; introducir RabbitMQ desde el inicio añadiría infraestructura sin un requisito actual de distribución de mensajes.

### Integraciones externas mediante adaptadores configurables

Los adaptadores utilizarán clientes HTTP admitidos por el harness y configuración inyectada mediante Options. El correo se enviará mediante SMTP configurable. La búsqueda de metadatos integrará IMDb y TMDB, con capacidad de añadir otros proveedores configurados. La ingestión IPTV leerá el directorio `streams` del repositorio `iptv-org/iptv` en GitHub y recibirá los países habilitados mediante configuración. Las credenciales de las integraciones (contraseña SMTP, claves de IMDb/TMDB) forman parte de la configuración en base de datos y se almacenan cifradas (véase «Configuración por capas»); nunca estarán en el código ni en los logs.

**Alternativas consideradas:** integrar directamente una plataforma en la lógica de negocio impediría sustituir proveedores y complicaría las pruebas.

### Sesiones, auditoría y seguridad

Las sesiones se validarán en el backend. Las contraseñas se almacenarán mediante un algoritmo de hash adecuado para contraseñas; nunca se guardarán en texto claro ni con cifrado reversible. Los logs evitarán contraseñas, tokens y datos personales innecesarios. La IP reenviada por nginx solo se considerará fiable cuando la petición proceda de un proxy configurado como confiable; esa IP alimentará los eventos de auditoría requeridos.

La estimación de entropía se calculará en la interfaz para actualizarse mientras se escribe, pero la política de contraseña se validará también en el backend. Se limitarán tamaño y frecuencia de peticiones y se validarán tipos, formatos y rangos.

**Alternativas consideradas:** confiar en cualquier encabezado de IP reenviado permitiría falsificar la dirección registrada; confiar únicamente en la validación del cliente permitiría omitir la política de contraseña.

### Acceso al streaming y Chromecast

La API entregará los medios sin exponer rutas del sistema de archivos y comprobará en cada petición de flujo que existe una sesión válida de un usuario registrado y activo. Un dispositivo Chromecast no comparte las cookies de sesión del navegador, por lo que, al enviar una reproducción, la API emitirá un permiso temporal firmado, ligado al usuario y al contenido, con una duración configurable en base de datos; el dispositivo lo presentará al solicitar el flujo y la API lo rechazará si ha caducado, si no coincide con el contenido o si el usuario ya no está activo. El remitente usará el SDK de Google Cast para web con el receptor multimedia por defecto, que reproduce HLS y MP4 H.264/AAC; la API deberá ser accesible por HTTPS desde la red del dispositivo y configurar CORS para el receptor.

**Alternativas consideradas:** reutilizar la cookie de sesión no funciona en el dispositivo; un enlace público permanente permitiría compartir los contenidos fuera de usuarios activos.

### Subtítulos, búsqueda e historial de visualización

La ingestión asociará los ficheros SRT y WebVTT con el mismo nombre base que el vídeo; la API servirá siempre WebVTT, convirtiendo SRT, y el reproductor mostrará la opción solo si existen. La búsqueda por texto usará las capacidades de PostgreSQL (búsqueda de texto completo y extensión `unaccent`, incluida en el script SQL), sin motor de búsqueda externo. El historial guardará, por usuario y contenido (película o episodio, no canales), la posición, el estado de visto y las fechas de auditoría; la interfaz enviará la posición con una frecuencia configurable y el umbral de visto será configurable (por defecto, el 90 % de la duración). El historial se elimina con el resto de datos de la cuenta.

**Alternativas consideradas:** un motor de búsqueda dedicado añadiría infraestructura sin necesidad para el volumen previsto; guardar la posición solo en el navegador impediría retomar en otro dispositivo.

### Observabilidad básica

La API ofrecerá un punto de comprobación de salud (`/api/v1/health`) que comprueba la base de datos sin revelar detalles. Los servicios usarán el registro estructurado de la plataforma .NET, sin contraseñas, tokens, valores sensibles ni datos personales innecesarios. Los trabajadores persistirán por proceso la última ejecución, duración, resultado y elementos procesados, que la administración consultará junto con su estado. Una pila externa de monitorización queda fuera de alcance.

**Alternativas consideradas:** incorporar OpenTelemetry y paneles externos desde el inicio requeriría ADR y operación adicional.

### Calidad, pruebas y contenedores

Los servicios backend tendrán pruebas unitarias con xUnit y pruebas de integración con Testcontainers; la interfaz tendrá pruebas E2E con Playwright. La cobertura unitaria será al menos del 80 %. CI ejecutará Roslyn analyzers, `dotnet format`, ESLint, Prettier, compilación TypeScript y las pruebas requeridas por el harness. Los servicios se empaquetarán con Docker.

**Alternativas consideradas:** pruebas solo unitarias no verificarían integraciones con PostgreSQL y el recorrido E2E; otros runners y herramientas de calidad no son los admitidos por el harness.

## Risks / Trade-offs

- [SMTP, IMDb y TMDB pueden cambiar sus requisitos de acceso o limitar las peticiones] → Mantener adaptadores independientes, guardar las credenciales cifradas en la configuración (nunca en el código) y tratar explícitamente errores y límites de cada proveedor.
- [La configuración en base de datos hace que la caída de la base de datos impida arrancar y que un valor erróneo se propague en el siguiente reinicio] → Fallo rápido con error sin datos sensibles, valores iniciales por defecto en el script SQL y pruebas de arranque.
- [Las credenciales almacenadas en base de datos amplían el impacto de una filtración de copias de seguridad] → Cifrarlas con una clave ajena a la base de datos y no registrarlas ni devolverlas en claro.
- [La eliminación de cuenta puede entrar en tensión con la retención de auditorías] → Diseñar registros con minimización de datos y asegurar que la información personal asociada se elimine dentro del plazo de borrado especificado.
- [Los procesos de ingestión pueden ser de larga duración o fallar parcialmente] → Ejecutarlos fuera de las peticiones, persistir su estado y permitir reintentos controlados sin duplicar registros.
- [Chromecast requiere que el dispositivo alcance la API por HTTPS y recibe un permiso temporal que podría compartirse mientras esté vigente] → Duración corta del permiso, ligado a usuario y contenido, y revocado al dejar de estar activo el usuario; documentar los requisitos de red.
- [La reproducción en streaming depende de formatos y medios disponibles en las fuentes] → Mantener la entrega de medios separada de la API de catálogo y validar HLS y MP4/H.264/AAC con los medios disponibles.
- [El uso de cookies exige protección frente a solicitudes cruzadas] → Aplicar controles de origen y protección CSRF en las operaciones que cambian estado.

## Migration Plan

No hay código ni datos existentes que migrar. La puesta en marcha deberá:

1. Crear la estructura `backend/` y `frontend/`, con los proyectos y pruebas iniciales.
2. Definir el esquema PostgreSQL y su script SQL fechado, incluidos los usuarios de base de datos exigidos y la tabla de configuración con sus valores iniciales.
3. Configurar los proveedores (JSON, entorno, ficheros de secretos y base de datos), con la cadena de conexión y la clave de cifrado en ficheros de secretos fuera del repositorio (secretos de Docker en local y CI), CORS, nginx y los servicios Docker para entornos locales y CI.
4. Implementar y verificar primero los contratos de identidad, consentimiento y sesiones; después incorporar catálogo, ingestión, reproducción, administración y operación.
5. Desplegar la versión inicial con una estrategia de reversión a la imagen anterior y respaldo/restauración de PostgreSQL; comprobar las políticas de eliminación antes de habilitar datos de usuarios reales.
