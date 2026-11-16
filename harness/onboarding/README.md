# Proceso de onboarding

Prepara un espacio de trabajo nuevo para trabajar con el harness. Lo ejecuta el agente (comando `/onboarding` en Claude Code), pidiendo confirmación al usuario antes de acciones con efecto externo (crear el repositorio, cambiar su configuración, instalar software).

## Cuándo se desencadena

1. El espacio de trabajo **no es un repositorio git**, o
2. es un repositorio git que **solo contiene el commit inicial**,

y no existe el marcador `harness/.onboarded`. El hook de inicio de sesión lo avisa automáticamente.

## Datos que se solicitan al usuario (uno a uno)

1. **Usuario de GitHub** → se obtiene con `gh api users/<usuario>` el nombre completo (`name`) y el correo *noreply* (`<id>+<usuario>@users.noreply.github.com`) para atribuirle los cambios. Si el usuario no tiene nombre público, se le pregunta.
2. **Nombre del repositorio.**
3. **Nombre del producto / proyecto.**
4. **Descripción del producto / proyecto.**
5. **Tipo de proyecto** que contendrá el repositorio (uno o varios: Python, C#, React).

## Ejecución (con todos los datos reunidos)

1. **Herramientas**: comprobar `git`, `dotnet`, `python3`, `openspec`, `node`, `npm`, `gh`, `docker` (según el tipo de proyecto) e instalar las que falten. **Nunca mono.** Python con entorno virtual.
2. **Git**: `git init -b main` si no es repositorio.
3. **Identidad local** (no global): `git config --local user.name …` / `user.email …` con los datos del paso 1. Activar los hooks de git: `git config --local core.hooksPath harness/hooks/git`.
4. **`gh`**: `gh auth status`; si no hay identidad válida, `gh auth login` de forma interactiva.
5. **OpenSpec**: `openspec init --tools claude` y generar `openspec/config.yaml` desde [templates/openspec/config.yaml.tmpl](../templates/openspec/config.yaml.tmpl) para que refleje las reglas del harness.
6. **Repositorio público** en GitHub si no existía: `gh repo create <nombre> --public --description "<descripción>"` (con confirmación del usuario). Commit inicial `chore: initial commit` en `main` y push (es el único commit/push permitido directamente a `main`).
7. **Configuración del repositorio**: `python3 harness/onboarding/scripts/github_setup.py settings <owner>/<repo>`. Revisar el informe: lo marcado `MANUAL` (sponsorships, permisos de issues/PR, etc.) no es configurable por API y se indica al usuario.
8. **Rulesets** (protección de `main` y de `release/v*`): `python3 harness/onboarding/scripts/github_setup.py rulesets <owner>/<repo> --types <python,csharp,react>`. Requiere que existan los workflows del paso 9 para poder resolver los *status checks*.
9. **Scaffolding** (en la rama `chore/scaffolding`, integrada con PR; el administrador puede hacer bypass):
   - Directorios `backend/` y `frontend/` en la raíz con los proyectos del tipo elegido, usando solo las tecnologías de [technologies.md](../rules/technologies.md), arquitectura hexagonal, DI por constructor y patrón Options.
   - C#: strong name. Generar la clave **fuera del repositorio** con [gen_snk.py](scripts/gen_snk.py) y guardarla como secreto `STRONG_NAME_KEY` de GitHub (`base64 -w0 key.snk | gh secret set STRONG_NAME_KEY`).
   - Workflows (desde [templates/github/workflows](../templates/github/workflows/README.md)): `pr.yml` (checks `quality`, `unit-tests`, `integration-tests` solo con backend, `pr-title`), `e2e.yml` (si hay frontend) y `release.yml`.
   - `.github/dependabot.yml` desde [templates/github/dependabot.yml](../templates/github/dependabot.yml) (filtros LTS; sin desactivar las actualizaciones de seguridad).
   - `docs/` desde [templates/docs](../templates/docs/README.md), `.env.example` y, si hay base de datos, el script `<yymmdd>.sql` desde [templates/sql](../templates/sql/README.md).
   - Tras integrar, activar CodeQL: `github_setup.py codeql <owner>/<repo>`.
10. **`.gitignore`** según [templates/docs/gitignore.md](../templates/docs/gitignore.md).
11. **`readme.md`** con descripción, objetivos y enlaces a la documentación (desde la plantilla `readme.md.tmpl`).

## Cierre

1. Escribir el marcador `harness/.onboarded` (JSON con fecha, repositorio y tipos de proyecto). **Desde ese momento el harness queda protegido por los hooks**: solo se puede modificar con un ADR (`harness-change: true` en la cabecera) en `docs/adr/`.
2. Resumir al usuario qué se hizo, qué queda manual y los resultados de cada paso.

## Directorios relacionados

- [scripts/](scripts/README.md): automatizaciones del onboarding y de las releases.
- [../templates/](../templates/README.md): plantillas que se instancian.
