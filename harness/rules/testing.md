# Desarrollo y ejecución de pruebas

- Obligatorias en todo proyecto: backend → unitarias **e** integración; frontend → **E2E**.
- Unitarias: en cada commit, cobertura **≥ 80 %**. En CI en cada PR hacia `main`; si fallan o no alcanzan cobertura, el merge queda bloqueado.
- Linter, formato y tipado estático (ver `technologies.md`): obligatorios en CI en cada PR hacia `main`; bloquean el merge.
- Integración: en cada PR hacia `main`; bloquean el merge.
- **Excepción**: PRs que solo modifiquen documentación (`docs/`, ficheros markdown y especificaciones OpenSpec) no ejecutan las pruebas de integración. El workflow **se ejecuta siempre** y en esos casos termina con éxito sin lanzarlas, para que la comprobación requerida quede reportada.
- E2E: después de cada merge a `main`.
