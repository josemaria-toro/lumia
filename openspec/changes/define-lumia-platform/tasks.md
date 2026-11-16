# Tasks

## 1. Scaffolding y plataforma

- [ ] 1.1 Crear los proyectos iniciales C#/.NET y React/TypeScript en `backend/` y `frontend/`, documentar mediante ADR el host HTTP y cualquier tecnología no incluida en `harness/rules/technologies.md`, y verificar compilación con `dotnet build` y el comando de build del frontend.
- [ ] 1.2 Preparar la configuración por Options con los proveedores de ficheros JSON, variables de entorno, ficheros de secretos y base de datos (carga única al iniciar la API y el trabajador, fallo de arranque si no carga, cadena de conexión y clave de cifrado solo en ficheros de secretos, valores sensibles cifrados y sin registrarse en claro) y los servicios Docker para desarrollo; verificar precedencia, arranque correcto y fallido con pruebas unitarias y de integración, y la validación del motor Docker elegido sin credenciales reales.
- [ ] 1.3 Crear el esquema inicial PostgreSQL con nombres `snake_case`, campos de auditoría y roles de base de datos requeridos, además de la tabla de configuración con valores iniciales, y verificar la creación desde cero mediante el script SQL fechado y una prueba de integración.
- [ ] 1.4 Redactar los ADR que justifiquen el SDK de Google Cast para web y no soportar ficheros ini ni xml como proveedores de configuración (solo JSON, entorno, ficheros de secretos y base de datos) y el almacenamiento cifrado de credenciales en base de datos; verificar que se numera correlativamente en `docs/adr/`.
- [ ] 1.5 Crear la documentación inicial en `docs/` (arquitectura, modelos y guía de desarrollo) y actualizar el README en español; documentar todas las claves de configuración, su origen y qué valores son sensibles, y verificar que los enlaces y comandos documentados existen.

## 2. Cuentas, autenticación y privacidad

- [ ] 2.1 Implementar registro, validación de edad y contraseña, indicador de entropía, bloqueo de correos temporales, activación y correo SMTP configurable; verificar casos permitidos y rechazados con pruebas unitarias, de integración y la documentación del API en `docs/`.
- [ ] 2.2 Implementar inicio de sesión, feature flag, bloqueo tras tres fallos, recuperación con token de 30 minutos y auditoría de accesos/altas con IP de nginx, user-agent y tipo de dispositivo; verificar autorización, fallos y datos auditados con pruebas y documentación en `docs/`.
- [ ] 2.3 Implementar sesiones mediante cookie, renovación por actividad cada cinco minutos, expiración por inactividad a los 30 minutos y límite absoluto de ocho horas; verificar expiraciones, redirección al inicio y protección de operaciones con pruebas y documentación.
- [ ] 2.4 Implementar aceptación de cookies, control de versión vigente de privacidad e historial de aceptación, además de selección español/inglés pública y privada; verificar escenarios de consentimiento e idioma con pruebas y documentación de usuario.
- [ ] 2.5 Implementar solicitud y reversión de baja, baja a los 15 días, borrado de datos (incluido el historial de visualización) 30 días después y bloqueo de nuevo registro mientras existan datos; verificar los límites temporales y eliminación de datos personales con pruebas de integración y documentación.

## 3. Catálogo, administración y favoritos

- [ ] 3.1 Implementar inicio público/privado, filtros por tipo, búsqueda por texto (sin distinguir mayúsculas ni acentos, combinable con el filtro, solo para usuarios autenticados, con PostgreSQL y la extensión `unaccent` en el script SQL), tarjetas informativas y paginación dinámica por scroll; verificar filtros, búsqueda y carga de páginas con pruebas de API y E2E, y documentar el catálogo en `docs/`.
- [ ] 3.2 Implementar roles de administrador y colaborador, CRUD autorizado y permisos de grano fino por acción y tipo de contenido, incluida la reasignación de metadatos; verificar denegaciones y permisos diferenciados para películas/series con pruebas de integración y documentación administrativa.
- [ ] 3.3 Implementar marcado, desmarcado y pantalla de favoritos por usuario; verificar que cada usuario solo consulta y modifica su propia lista con pruebas de API y E2E, y documentar su uso.
- [ ] 3.4 Implementar el historial de visualización: posición de películas y episodios (no canales), reanudación, sección de continuar viendo, marca de visto por umbral configurable (90 % por defecto), siguiente episodio y gestión del historial propio; verificar con pruebas de API y E2E que cada usuario solo accede al suyo y que la baja lo elimina, y documentar su uso.

## 4. Ingestión y reproducción multimedia

- [ ] 4.1 Implementar el escaneo de películas y series en rutas configurables cada 30 minutos, respetando carpetas/temporadas y referencias a archivos físicos; verificar detección, actualización y archivos múltiples por carpeta con pruebas del trabajador y de integración, y documentar la configuración (en base de datos, aplicada tras reiniciar el trabajador).
- [ ] 4.2 Implementar adaptadores configurables para consultar IMDb y TMDB y asociar metadatos a archivos; verificar resultados, errores y sustitución de correspondencia con dobles de prueba y pruebas de integración, y documentar credenciales/cuotas en `docs/` sin secretos.
- [ ] 4.3 Implementar la descarga diaria de listas IPTV desde `iptv-org/iptv/streams` para los países configurados; verificar que solo se incorporan los países seleccionados y que fallos de red no dañan el catálogo mediante pruebas y documentación de Options (los cambios de países se aplican al reiniciar el trabajador).
- [ ] 4.4 Implementar reproducción HLS para canales y MP4/H.264/AAC para películas y series, con controles de reproducir, pausar, detener, pantalla completa, siguiente episodio/canal y carrusel; verificar los flujos compatibles mediante pruebas del reproductor y E2E, y documentar formatos admitidos.
- [ ] 4.5 Restringir la entrega de flujos (incluidos canales) a usuarios registrados y activos sin exponer rutas del servidor, con revocación si la sesión expira; verificar visitantes, cuentas no activas y sesiones expiradas con pruebas de integración y E2E, y documentar el modelo de acceso.
- [ ] 4.6 Implementar subtítulos opcionales: detección SRT/WebVTT por nombre base en la ingestión, servicio en WebVTT y selector en el reproductor solo si existen; verificar contenidos con y sin subtítulos con pruebas del trabajador y E2E, y documentar los formatos admitidos.
- [ ] 4.7 Implementar la reproducción en Chromecast con el SDK de Google Cast y permisos temporales firmados por usuario y contenido (duración configurable, revocados al dejar de estar activo el usuario); verificar caducidad, denegación sin permiso y regreso al navegador con pruebas de integración y manuales con dispositivo, y documentar los requisitos de red (HTTPS y CORS).

## 5. Operación y experiencia de usuario

- [ ] 5.1 Implementar la programación de la página de mantenimiento y la consulta administrativa del estado de procesos en segundo plano; verificar activación programada, permisos y estado tras reinicio con pruebas de integración y documentación operativa.
- [ ] 5.2 Aplicar identidad visual, fondos, logotipo y personaje animado, y adaptar todas las pantallas a móvil/escritorio y WCAG 2.0 AA; verificar recorridos con Playwright y comprobaciones de accesibilidad, y documentar las pautas visuales en `docs/`.
- [ ] 5.3 Implementar la comprobación de salud (`/api/v1/health`), los registros estructurados sin datos sensibles y las métricas persistidas de los procesos en segundo plano consultables por el administrador; verificar salud operativa/no operativa, ausencia de datos sensibles en logs y métricas tras fallos con pruebas de integración, y documentar la operación.

## 6. Integración y calidad

- [ ] 6.1 Configurar CI para pruebas unitarias con cobertura mínima del 80 %, integración de backend, E2E de frontend, linters, formato, tipado y validación de títulos de PR; verificar cada comprobación en una ejecución de CI y documentar su uso.
- [ ] 6.2 Ejecutar los recorridos integrados de registro, activación, consentimiento, sesión, navegación, favoritos, historial, búsqueda, administración, ingestión, reproducción (con subtítulos y Chromecast) y observabilidad; verificar criterios de aceptación y confirmar que las suites unitarias, de integración y E2E pasan antes de solicitar la revisión.
