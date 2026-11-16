# Scripts de onboarding

Solo usan la biblioteca estándar de Python y `gh`/`openssl`.

| Script | Propósito |
|:-------|:----------|
| `github_setup.py` | Configura ajustes y rulesets del repositorio (`settings`, `rulesets`, `codeql`). Informa de lo que debe hacerse a mano. |
| `gen_snk.py` | Genera una clave de strong name `.snk` temporal sin mono. La clave no se versiona. |
| `next_version.py` | Calcula la versión de la próxima release (SemVer) a partir de los commits convencionales de `main`; sale con código 3 si no hay release que generar. |
