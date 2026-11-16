# Versionado y releases

## SemVer 2.0.0 (`MAJOR.MINOR.PATCH`)
- MAJOR: commits con `!` o `BREAKING CHANGE:`. MINOR: `feat`. PATCH: `fix`.
- La versión **no se guarda en ningún fichero**: se calcula en cada release a partir de la release anterior y de los commits convencionales integrados en `main` desde entonces. Se aplica el incremento mayor y los niveles inferiores se reinician a 0.
- Sin release previa: **0.1.0**. Si no hay commits que justifiquen incremento (solo docs, chore, test, ci…), **no se genera release**.

## Generación de artefactos
Se desencadena cuando se solicita una nueva release al agente:
1. Calcular la versión (`harness/hooks`/`onboarding/scripts/next_version.py` ayuda a hacerlo).
2. Crear la rama `release/v<version>` desde `main`.
3. La pipeline construye los artefactos con la versión calculada.

Para C#, Python y React: un **zip por artefacto desplegable**, incluido en la release de GitHub junto con las **instrucciones de configuración e instalación**. C#: configuración Release y sin símbolos de depuración.
