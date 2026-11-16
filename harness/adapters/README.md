# Adaptadores

Un adaptador por herramienta, **fino**: solo conecta la herramienta con `harness/` sin copiar reglas.

| Herramienta | Documentación | Ficheros fuera de `harness/` |
|:------------|:--------------|:-----------------------------|
| Claude Code | [claude-code/](claude-code/README.md) | `CLAUDE.md`, `.claude/settings.json`, `.claude/commands/onboarding.md` |

Para añadir una herramienta: crea `adapters/<herramienta>/README.md`, el fichero de instrucciones que la herramienta requiera (referenciando `harness/rules/`) y registra sus hooks con `harness/hooks/run.py` (ver [hooks](../hooks/README.md)).
