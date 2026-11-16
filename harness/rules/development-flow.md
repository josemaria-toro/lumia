# Guía de desarrollo (OpenSpec, uso obligatorio)

Flujo con cuatro fases. Para cerrar cada una se requiere **confirmación del usuario** y **no pueden quedar preguntas abiertas**: si las hay, se ofrece registrarlas en `docs/technical-debt.md` (registrarlas no bloquea el cierre de la fase).

1. **Exploración**: conversación para definir las especificaciones.
2. **Propuesta**: propuesta y diseño de la solución. Se crea una rama propia (ver `branching.md`) y un primer commit (local y remoto) que persista propuesta y diseño.
3. **Implementación**: se genera todo el código, infraestructura y cambios. Commit (local y remoto) y PR hacia `main`. La fase no termina hasta que las pruebas de integración de la PR pasen.
4. **Archivado**: archivado de especificaciones en rama propia integrada en `main` mediante PR. **No se puede iniciar otra especificación si hay alguna pendiente de archivar.**

Las especificaciones funcionales y técnicas se escriben en **español**.
