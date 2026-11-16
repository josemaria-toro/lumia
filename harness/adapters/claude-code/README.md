# Adaptador de Claude Code

Claude Code exige que ciertos ficheros vivan fuera de `harness/`. Son solo punteros:

| Fichero | Función |
|:--------|:--------|
| `CLAUDE.md` | Importa (`@harness/rules/*.md`) las reglas. No contiene reglas propias. |
| `.claude/settings.json` | Registra los hooks (`SessionStart`, `PreToolUse` para `Bash` y `Write\|Edit\|MultiEdit\|NotebookEdit`) que llaman a `harness/hooks/run.py claude …`, y deniega lecturas de secretos y comandos destructivos. |
| `.claude/commands/onboarding.md` | Comando `/onboarding` que apunta a `harness/onboarding/README.md`. |

## Notas

- Los hooks bloquean con código de salida 2; Claude recibe el motivo y debe corregir la acción.
- Si cambian las reglas, se edita `harness/rules/` y el adaptador no necesita cambios (salvo añadir nuevos ficheros a los `@imports`).
- OpenSpec (`openspec init --tools claude`) añade sus propios comandos/skills en `.claude/`; no forman parte del adaptador.
- Estos ficheros están protegidos tras el onboarding (ver `harness/hooks/lib/common.py`, `PROTECTED`).
