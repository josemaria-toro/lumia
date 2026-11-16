# Hooks (guardarraíles)

Implementados una sola vez en Python (solo biblioteca estándar) y reutilizados por cada herramienta.

```
hooks/
├── run.py        # punto de entrada de agentes: run.py <agente> <bash|file|session-start>
├── lib/          # reglas puras, utilidades de git/onboarding y normalización de eventos por agente
├── guards/       # shell.py, files.py, session.py
└── git/          # hooks de git (independientes del agente)
```

Código de salida `2` = acción bloqueada (el motivo se muestra al agente); `0` = permitida.

## Qué se verifica

**Shell** (`guards/shell.py`): commits y títulos de PR en Conventional Commits, en inglés y sin atribución de agente; sin `--no-verify`; sin commit/push/merge directo en `main` (salvo el commit inicial del onboarding); sin force push; nombres de rama válidos; no borrar `main`/`release/*`; identidad local de git obligatoria y sin `git config --global`; `gh pr merge` solo con `--squash` (sin `--admin`/`--auto`); tags de release `vX.Y.Z`; sin mostrar tokens ni pasar secretos por argumentos; sin mono; pip solo en entorno virtual; sin migraciones; sin abrir otra especificación con otras pendientes de archivar; harness protegido tras el onboarding.

**Ficheros** (`guards/files.py`): sin secretos ni ficheros de claves/`.env`; scripts SQL `<yymmdd>.sql` (solo se añade al final con `ALTER`); sin migraciones; importaciones Python (relativas en `__init__.py`, absolutas en el resto); harness protegido tras el onboarding.

**Sesión** (`guards/session.py`): informa de onboarding pendiente, rama actual y especificaciones sin archivar.

**Git** (`git/`): `commit-msg`, `pre-commit` y `pre-push` aplican las mismas reglas aunque se use otra herramienta. Se activan en el onboarding con `git config --local core.hooksPath harness/hooks/git`.

## Añadir un agente

1. Añade `from_<agente>` en `lib/events.py` y la rama correspondiente en `run.py`.
2. Registra en la configuración del agente los comandos `python3 harness/hooks/run.py <agente> <guard>`.
3. Documéntalo en `adapters/`.
