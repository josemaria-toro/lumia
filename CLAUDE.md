# Harness de vibecoding (adaptador Claude Code)

Este fichero es un adaptador fino: la **única fuente de verdad** es el directorio [harness/](harness/README.md). No dupliques reglas aquí.

Reglas obligatorias (cárgalas y respétalas):

@harness/rules/github.md
@harness/rules/architecture.md
@harness/rules/branching.md
@harness/rules/commits.md
@harness/rules/development-flow.md
@harness/rules/code-style.md
@harness/rules/configuration.md
@harness/rules/documentation.md
@harness/rules/technologies.md
@harness/rules/testing.md
@harness/rules/data-models.md
@harness/rules/versioning-and-releases.md
@harness/rules/security.md

Otros puntos de entrada:
- Onboarding: [harness/onboarding/README.md](harness/onboarding/README.md) (comando `/onboarding`).
- Los hooks de `.claude/settings.json` ejecutan `harness/hooks/run.py` y bloquean las acciones que incumplen estas reglas. Si un hook bloquea una acción, corrige la acción; nunca intentes evitar el hook.
- Tras el onboarding, el harness solo se modifica con un ADR (`harness-change: true`).
