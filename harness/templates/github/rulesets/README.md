# Rulesets

Los rulesets no se mantienen como ficheros estáticos: se generan desde `onboarding/scripts/github_setup.py rulesets`, que es la definición ejecutable.

- **Protect main**: bypass del administrador; sin borrado ni force push; historial lineal; PR con 1 aprobador, reset de aprobaciones, aprobación de los últimos cambios, conversaciones resueltas y solo squash; CodeQL (alto o superior, errores); calidad de código (errores); status checks (`quality`, `unit-tests`, `pr-title` y, con backend, `integration-tests`).
- **Protect releases** (`release/v*`): bypass del administrador; sin borrado, sin actualización y sin force push.
