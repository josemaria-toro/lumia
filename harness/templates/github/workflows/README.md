# Workflows

Se conservan solo los bloques marcados `# [python]`, `# [csharp]`, `# [react]` de los tipos de proyecto elegidos.

| Fichero | Cuándo | Jobs (status checks requeridos) |
|:--------|:-------|:--------------------------------|
| `pr.yml` | PR hacia `main` | `pr-title`, `quality`, `unit-tests`, `integration-tests` (solo backend). Siempre se ejecuta; si la PR solo toca documentación, `integration-tests` termina en éxito sin lanzar pruebas. |
| `e2e.yml` | Tras cada merge a `main` | `e2e` (solo frontend, Playwright) |
| `release.yml` | Creación de `release/v*` | Construye, comprime un zip por artefacto y publica la release con las instrucciones de instalación (`docs/installation.md`). |

Los nombres de los jobs deben coincidir con los *status checks* del ruleset (ver `onboarding/scripts/github_setup.py`).
