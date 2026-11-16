# Seguridad

Referencias: OWASP ASVS (aplicaciones) y OWASP API Security Top 10 (APIs). Cada proyecto evalúa además sus amenazas y datos sensibles; esto es una base, no sustituye ese análisis.

## Todos los proyectos
- **Secretos**: nunca en código, logs ni repositorio (contraseñas, tokens, claves privadas, cadenas de conexión con credenciales). Variables de entorno o gestor de secretos; `.env.example` sin valores reales. Mínimo acceso; rotar si se expone.
- **Dependencias**: versiones fijadas/reproducibles, revisar vulnerabilidades; no instalar paquetes sin justificar origen y necesidad.
- **Validación y errores**: validar en los límites; no exponer stack traces, secretos ni detalles internos.
- **Permisos**: mínimo privilegio. PostgreSQL con cuentas distintas por función; limitar permisos de RabbitMQ.
- **Comunicaciones**: TLS en redes no confiables; no registrar datos sensibles.
- **CI/CD**: análisis de código y dependencias; proteger credenciales de pipelines; restringir quién publica releases.
- **Pruebas**: cubrir autorización, validación y fallos; corregir vulnerabilidades críticas/altas antes de publicar.

## APIs
- Rutas `/api/v<num-version>/<path>` (p. ej. `/api/v1/auth/login`).
- Autenticación y autorización por caso de uso; permisos en cada operación y recurso.
- Límite de tamaño y frecuencia; validar tipos, formatos y rangos.
- Consultas parametrizadas; proteger comandos del sistema y rutas de archivos.
- CORS solo para orígenes necesarios; sin información sensible en respuestas.
- Contraseñas con hash apropiado (nunca texto claro ni cifrado reversible).

## Consolas y procesos en segundo plano
- Sin secretos como argumentos de línea de comandos.
- Validar archivos y rutas; no leer/sobrescribir fuera de lo previsto.
- Tareas programadas y consumidores RabbitMQ: permisos limitados, reintentos controlados, sin bucles por mensajes inválidos.
