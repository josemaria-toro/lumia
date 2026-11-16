# Harness de vibecoding

**Única fuente de verdad** de las reglas, guardarraíles y procesos que siguen los agentes de IA al crear proyectos. Cada herramienta (Claude Code, etc.) tiene solo un **adaptador fino** que apunta aquí; las reglas nunca se duplican.

| Directorio | Contenido |
|:-----------|:----------|
| [rules/](rules/README.md) | Reglas normativas (arquitectura, ramas, commits, flujo OpenSpec, estilo, pruebas, datos, releases, seguridad…). |
| [hooks/](hooks/README.md) | Guardarraíles ejecutables: hooks de agente y hooks de git. |
| [onboarding/](onboarding/README.md) | Proceso de onboarding y sus scripts. |
| [templates/](templates/README.md) | Plantillas (workflows, dependabot, OpenSpec, docs, SQL). |
| [adapters/](adapters/README.md) | Cómo se conecta cada herramienta con el harness. |

## Principios

1. Una sola fuente: se edita `harness/`; los adaptadores solo referencian.
2. Lo que se puede verificar automáticamente, se verifica con hooks (defensa en profundidad: hooks del agente + hooks de git + CI).
3. Tras el onboarding el harness solo se modifica con un ADR (`harness-change: true`); los hooks lo hacen cumplir.
