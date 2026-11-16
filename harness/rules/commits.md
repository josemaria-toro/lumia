# Convención de commits

- Mensajes de commit y títulos de PR siguen **Conventional Commits**: `type(scope): description` (scope opcional).
- Tipos admitidos: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Cambios incompatibles: `!` tras el tipo o scope, o pie `BREAKING CHANGE:`.
- El merge a `main` es con **squash** y el mensaje por defecto es el título de la PR: el título debe cumplir siempre la convención (se valida en CI).
- Commits y títulos se escriben en **inglés**.
- **Los agentes tienen prohibido atribuirse los cambios**: sin `Co-Authored-By` de agente, sin «Generated with…», ni en commits ni en PRs. La autoría es del usuario (identidad local de git).
