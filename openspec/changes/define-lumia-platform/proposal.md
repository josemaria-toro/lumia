# Proposal

## Why

Lumia necesita convertir la visión funcional de `lumia.md` en contratos verificables antes de implementar una plataforma de streaming nueva. La especificación separará las capacidades del producto y conservará sus reglas de negocio, seguridad, operación y experiencia de usuario como criterios de aceptación.

## What Changes

- Definir el ciclo de vida de cuentas: autenticación, registro, recuperación de contraseña y baja.
- Especificar sesiones, consentimiento de privacidad y selección de idioma.
- Definir navegación y descubrimiento de contenidos, ingestión de medios, reproducción y favoritos.
- Especificar administración de contenidos y permisos, mantenimiento programado y directrices visuales.
- Restringir la reproducción a usuarios registrados y activos, añadir búsqueda por texto, subtítulos opcionales, reproducción en Chromecast e historial de visualización (continuar viendo).
- Añadir comprobación de salud, registros estructurados y métricas de los procesos en segundo plano.
- Especificar la configuración: proveedores de variables de entorno, ficheros JSON, ficheros de secretos y base de datos, con la cadena de conexión y la clave de cifrado en ficheros de secretos y el resto de la configuración cargada desde ella al iniciar.
- Establecer escenarios verificables para restricciones, auditoría, expiraciones y actualización de contenido.

## Capabilities

### New Capabilities

- `account-authentication`: Inicio de sesión, activación previa de cuenta, bloqueo tras intentos fallidos, recuperación de contraseña y auditoría de accesos.
- `account-registration`: Alta, validación de edad y contraseña, detección de correo temporal, verificación de correo y auditoría.
- `account-deletion`: Solicitud de baja, periodo de reversión, eliminación de cuenta y borrado posterior de datos.
- `user-sessions`: Sesiones identificadas mediante cookies con expiración por inactividad y límite máximo de duración.
- `privacy-consent`: Aceptación de cookies y de la política de privacidad vigente con historial de versiones aceptadas.
- `localization`: Idiomas español e inglés con selección pública y preferencia del usuario autenticado.
- `content-discovery`: Inicio público y privado, filtros, búsqueda por texto, tarjetas informativas y paginación dinámica.
- `media-ingestion`: Detección de películas, series y sus subtítulos en rutas configurables, consulta de metadatos externos e importación periódica de canales.
- `media-playback`: Reproducción en streaming restringida a usuarios registrados y activos, controles multimedia, subtítulos opcionales, Chromecast y cambio de episodio o canal.
- `watch-history`: Posición de reproducción, reanudación, continuar viendo, contenido visto y gestión del historial propio.
- `favorites`: Marcado, desmarcado y gestión de contenidos favoritos.
- `content-administration`: Gestión de contenidos y permisos administrativos de grano fino para administradores y colaboradores.
- `platform-maintenance`: Página de mantenimiento programable, estado y métricas de procesos en segundo plano, comprobación de salud, registros estructurados y consideración del proxy inverso.
- `platform-configuration`: Proveedores de configuración (entorno, JSON, ficheros de secretos y base de datos), cadena de conexión y clave de cifrado en ficheros de secretos, carga al iniciar y cifrado de valores sensibles.
- `visual-experience`: Identidad visual, fondos temáticos y personaje animado de la pantalla de inicio.

### Modified Capabilities

Ninguna. El repositorio no contiene especificaciones existentes.

## Impact

El repositorio solo contiene documentación de producto y configuración OpenSpec; no se encontró una implementación de Lumia. Estos artefactos establecerán los contratos para futuras interfaces, persistencia, correo electrónico, proveedores de metadatos, fuentes IPTV, procesamiento en segundo plano, proxy nginx, configuración almacenada en base de datos y experiencia web. La selección de proveedores y tecnologías concretos queda fuera de esta propuesta cuando `lumia.md` no los determina.
