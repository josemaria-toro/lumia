# guards

Cada módulo expone `check(event) -> list[str]` con las infracciones detectadas (vacía = permitido). `session.py` expone `context(event)` para inyectar contexto al iniciar la sesión.
