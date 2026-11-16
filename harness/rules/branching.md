# Gestión de ramas

Rama persistente: `main`. Las ramas temporales salen de ella:

| Tipo    | Formato                   | Finalidad                                              |
|:--------|:--------------------------|:-------------------------------------------------------|
| Bug     | `bug/short-description`     | Resolver problemas del código actual                   |
| Change  | `change/short-description`  | Modificar el comportamiento de funcionalidades existentes |
| Chore   | `chore/short-description`   | Cambios que no son funcionalidad (p. ej. documentación) |
| Feature | `feature/short-description` | Nuevas funcionalidades                                 |
| Hotfix  | `hotfix/short-description`  | Problemas críticos de producción                       |
| Release | `release/v<version>`        | Foto fija del código del que se generan artefactos     |

- Nunca se hace commit ni push directo a `main` (excepto el commit inicial del onboarding).
- Nunca se hace force push.
- `short-description`: minúsculas, números y guiones.
