# Harness para vibecoding
El objetivo de este documento es definir el contenido del harness que será utilizado por los agentes de inteligencia artificial a la hora de crear proyectos de vibecoding.
## GitHub
GitHub será la plataforma de desarrollo que dara soporte a todos los repositorios, proyectos y despliegues. Para el acceso a esta plataforma se utilizará la herramienta 'gh', que ya contará con las credenciales necesarias para realizar todas las tareas y actividades necesarias.
## Arquitectura
Para todos los proyectos que se generen, la arquitectura admitida es la hexagonal, requiriendo el cumplimiento de los principios **SOLID**. La inyección de dependencias será obligatoria por diseño, por lo que todos los proveedores, servicios, configuraciones, etc., deben ser inyectables por el constructor. Para la inyección de la configuración en los constructores, el patrón a utilizar es Options, por lo que no estará admitido pasar parámetros de configuración a un constructor que no cumplan con este patrón.
## Gestión de ramas
Existirá una rama persistente 'main', que actuará como rama principal y a partir de ella, se sacarán las ramas temporales. Existirán también, varias ramas temporales, cada una para una finalidad concreta:
- **Bug**: rama para resolver problemas existentes en el código fuente actual. El formato para estas ramas es el siguiente: *bug/short-description*
- **Change**: rama para modificar el comportamiento de funcionalidades ya existentes. El formato para estas ramas es el siguiente: *change/short-description*
- **Chore**: rama para realizar cambios que no corresponden a funcionalidades, por ejemplo, modificación de la documentación. El formato para estas ramas es el siguiente: *chore/short-description*
- **Feature**: rama para el desarrollo de nuevas funcionalidades. El formato para estas ramas es el siguiente: *feature/short-description*
- **Hotfix**: rama para resolver problemas críticos de producción. El formato para estas ramas es el siguiente: *hotfix/short-description*

Adicionalmente, existirán un conjunto de ramas para la gestión de releases:
- **Release**: rama que contendrá una foto fija del código fuente a partir del cual, se han generado artefactos para su despliegue en producción. El formato para estas ramas es el siguiente: *release/v<version>*
## Convención de commits
Los mensajes de commit y los títulos de las pull requests seguirán la especificación de commits convencionales (Conventional Commits): *type(scope): description*, donde el scope es opcional. Los tipos admitidos son: feat, fix, docs, refactor, perf, test, build, ci, chore y revert. Los cambios que rompan compatibilidad se indicarán con `!` tras el tipo o scope, o con el pie *BREAKING CHANGE:*.  
Dado que el merge a 'main' se realiza con squash y el mensaje por defecto es el título de la pull request, este título debe cumplir siempre la convención. Su validación se realiza en CI. Los mensajes de commit y los títulos se escriben en inglés.
## Guía de desarrollo
El desarrollo guiado por agentes de inteligencia artificial se basará en el estándar de OpenSpec (uso obligatorio). El flujo a seguir será el siguiente:
- **Exploración**: fase del flujo consistente en una conversación con el agente de inteligencia artificial para definir las especificaciones. Es necesaria la confirmación del usuario para dar por terminada esta fase, además, no pueden quedar preguntas abiertas y en tal caso, se debe ofrecer al usuario incluirlas en un documento de deuda técnica. Lo incluido en este documento de deuda técnica, no bloquea la finalización de esta fase.
- **Propuesta**: fase del flujo consistente en la elaboración de la propuesta y el diseño de la solución a implementar. Es necesaria la confirmación del usuario para dar por terminada esta fase, además, no pueden quedar preguntas abiertas y en tal caso, se debe ofrecer al usuario incluirlas en un documento de deuda técnica. Lo incluido en este documento de deuda técnica, no bloquea la finalización de esta fase. En esta fase se deberá crear una rama propia, siguiendo la política de nombrado de ramas. Para evitar la posibilidad de perder los cambios realizados, se realizará un primer commit en la rama (local y remota) para persistir la propuesta y el diseño realizado, en git.
- **Implementación**: fase del flujo consistente en la implementación de la especificación, generando todo el código, infraestructura y cambios necesarios. Es necesaria la confirmación del usuario para dar por terminada esta fase, además, no pueden quedar preguntas abiertas y en tal caso, se debe ofrecer al usuario incluirlas en un documento de deuda técnica. Lo incluido en este documento de deuda técnica, no bloquea la finalización de esta fase. Para evitar la posibilidad de perder los cambios realizados, se realizará un commit en la rama (local y remota) para persistir los cambios en git y posteriormente, se debe abrir una pull request para integrar los cambios en la rama 'main'. La fase no se podrá dar por terminada hasta que las pruebas de integración de la pull request se hayan superado.
- **Archivado**: fase del flujo consistente en el archivado de las especificaciones. Esta fase requiere de una rama propia, que será integrada en 'main' a través de una pull request. No se podrá avanzar con otra especificación si otras especificaciones están pendientes de archivar.

> Los agentes de inteligencia artificial tendrán prohibido atribuirse los cambios del código fuente.
## Desarrollo en python
Este lenguaje de programación será utilizado para el desarrollo de aplicaciones de backend (consola, servicios o api's). El desarrollo en este lenguaje debe seguir las normas de PEP8. Las importaciones desde ficheros `__init__.py` debe realizarse utilizando rutas relativas y en el resto de ficheros, se ha de utilizar rutas absolutas. Las clases deben organizarse de la siguiente forma: miembros de clase primero, después constructores y métodos especiales, propiedades y por último los métodos. Tanto los métodos como las propiedades deben ordenarse alfabéticamente, los públicos primero y el resto después. Los proyectos de Python siempre deben utilizar un entorno virtual.
## Desarrollo en C#
Este lenguaje de programación será utilizado para el desarrollo de aplicaciones de backend (consola, servicios o api's). El desarrollo en este lenguaje debe seguir las normas definidas por Microsoft. Las clases deben organizarse de la siguiente forma: miembros de clase primero, después constructores y métodos especiales, propiedades y por último los métodos. Tanto los métodos como las propiedades deben ordenarse alfabéticamente, los públicos primero y el resto después. Los proyectos de C# deben firmarse con strong name por lo que las claves deben generarse temporalmente y la clave privada debe configurarse como variable de entorno en GitHub (no se podrá instalar mono).
## Desarrollo en react
Este lenguaje de programación será utilizado para el desarrollo de aplicaciones de frontend (web). El desarrollo en este lenguaje debe seguir las normas definidas en la guía oficial de react. Las clases deben organizarse de la siguiente forma: miembros de clase primero, después constructores y métodos especiales, propiedades y por último los métodos. Tanto los métodos como las propiedades deben ordenarse alfabéticamente, los públicos primero y el resto después. Todos los desarrollos en este lenguaje deben cumplir con ser responsivos y cumplir con la norma de accesibilidad WCAG 2.0 AA.
## Gestión de la configuración
Los proyectos deberán tener la capacidad de leer las configuraciones desde diferentes orígenes:
- Variables de entorno
- Ficheros (json, ini, xml)
- Ficheros de secretos
- Base de datos

Todas las configuraciones necesarias por los diferentes proyectos, deben quedar documentadas.
## Documentación
Todo proyecto debe disponer de documentación en Español, en formato markdown y versionado con el código fuente:
- Debe incluir el diagrama de arquitectura
- Debe incluir los diagramas de clase
- Debe incluir los diagramas de casos de uso
- Debe incluir la guía de construcción, configuración e instalación
- Debe incluir el fichero readme.md con la descripción y objetivos del proyecto, y enlaces a la documentación.
- Debe incluir los ADR (Architecture Decision Records) en el directorio 'docs/adr', un fichero markdown por decisión, numerados correlativamente (por ejemplo, 0001-titulo-corto.md).
- Debe incluir el documento de deuda técnica en 'docs/technical-debt.md', donde se registrarán las cuestiones abiertas que se decida aplazar durante las fases del flujo de desarrollo.

Toda la documentación del proyecto debe generarse en el directorio 'docs'.

El código fuente de los proyectos debe estar escrito y documentado en inglés y las especificaciones funcionales y técnicas, deben estar escritas en Español.  
La documentación de los proyectos debe quedar actualizada para poder crear una pull request.
## Tecnologías
Las tecnologías admitidas serán las siguientes:
- Cuando un proyecto requiera de acceso a base de datos, el motor aceptado es PostgreSQL
- Cuando un proyecto requiera de un broker de mensajería, el broker aceptado es RabbitMQ
- Para la contenerización de aplicaciones se utilizará Docker.

| Necesidad              | Python         | C#              | React      | Markdown |
|:-----------------------|:---------------|:----------------|:---------- |:---------|
| Diagramas              |                |                 |            | mermaid  |
| PostgreSQL             | asyncpg        | Npgsql          |            |          |
| RabbitMQ               | aio-pika       | RabbitMQ.Client |            |          |
| ORM                    | SQLAlchemy     | EntityFramework |            |          |
| Mocks                  | unittest.mock  | Moq             |            |          |
| Pruebas unitarias      | pytest         | xUnit           | Vitest     |          |
| Pruebas de integración | Testcontainers | Testcontainers  |            |          |
| Pruebas E2E            |                |                 | Playwright |          |
| Cobertura              | pytest-cov     | Coverlet        | Vitest     |          |
| Cliente HTTP           | httpx          | HttpClient      | fetch      |          |
| Linter                 | ruff           | Roslyn analyzers| ESLint     |          |
| Formato                | ruff format    | dotnet format   | Prettier   |          |
| Tipado estático        | mypy           | Compilador C#   | TypeScript |          |

> El uso de cualquier otra tecnología no incluida en el listado anterior, requiere de un ADR que justifique su uso.
## Desarrollo y ejecución de pruebas
El desarrollo de pruebas es obligatorio en cualquier tipo de proyecto:
- Para los proyectos de backend, son **obligatorias** las pruebas unitarias y de integración.
- Para los proyectos de frontend, son **obligatorias** las pruebas E2E.

La ejecución de las pruebas unitarias debe realizarse en cada commit y debe cubrir al menos el 80% del código. Esta comprobación se ejecuta en CI en cada pull request hacia main, y si no se supera (pruebas fallidas o cobertura inferior al 80%), el merge a main queda bloqueado.  
El linter, la comprobación de formato y el tipado estático indicados en la tabla de tecnologías son obligatorios y deben ejecutarse en CI en cada pull request hacia main. Si no se superan, el merge a main queda bloqueado.  
La ejecución de las pruebas de integración debe realizarse en cada pull request hacia main. Si las pruebas no se superan, el merge a main queda bloqueado.  
Excepción: las pull requests que solo modifiquen documentación (directorio 'docs', ficheros markdown y especificaciones de OpenSpec), como las de la fase de Archivado, no ejecutan las pruebas de integración. El workflow debe ejecutarse siempre y, en estos casos, finalizar con éxito sin lanzar las pruebas, para que la comprobación requerida quede reportada y no bloquee el merge.  
La ejecución de las pruebas E2E debe realizarse después de cada merge a main.  
## Definición de modelos de datos
Si un proyecto requiere de acceso a datos, el modelo debe definir sus tablas y columnas con la regla de nombrado **snake_case**.
Todas las tablas deben disponer de campos de auditoría:
- **created_at**: fecha de creación del registro (obligatorio)
- **created_by**: usuario que crea el registro (opcional)
- **updated_at**: fecha de modificación del registro (obligatorio)
- **updated_by**: usuario que realiza la modificación (opcional)

Las migraciones no están admitidas por lo que en cada modificación del modelo de datos, se debe generar un script con los cambios a aplicar en base de datos. El formato del fichero debe ser el siguiente: \<yymmdd\>.sql  
Si se realizan varios cambios en el mismo día, el fichero correspondiente a ese día, debe ser actualizado. La estructura de tablas y columnas ya definida en ese fichero no puede modificarse; los cambios se deben añadir al final con la orden `ALTER`.  
El script debe incorporar la creación de la base de datos y debe utilizar el nombre del producto. También debe incorporar la creación de 3 usuarios:
- **Administrador**: propietario de la base de datos
- **Usuario de la aplicacion**: puede realizar consultas, inserciones y actualizaciones.
- **Usuario de mantenimiento**: se comportará como el usuario de la aplicación pero también tendrá permitido el borrado de registros.
## Versionado de código y artefactos
El versionado seguirá el estándar de versionado semántico (SemVer 2.0.0): *MAJOR.MINOR.PATCH*.
- **MAJOR**: se incrementa cuando hay cambios que rompen la compatibilidad (commits con `!` o con el pie *BREAKING CHANGE:*).
- **MINOR**: se incrementa cuando se añaden funcionalidades manteniendo la compatibilidad (commits de tipo *feat*).
- **PATCH**: se incrementa cuando se corrigen errores manteniendo la compatibilidad (commits de tipo *fix*).

La versión no se mantiene en ningún fichero de forma permanente, sino que se calcula en cada release a partir de la versión de la release anterior y de los commits convencionales integrados en 'main' desde entonces; se aplica el incremento de mayor nivel que corresponda y los niveles inferiores se reinician a 0. Si no existe ninguna release anterior, la primera versión será la 0.1.0. Si desde la última release no hay commits que justifiquen un incremento (solo docs, chore, test, ci, etc.), no se generará la release.
## Generación y despliegue de artefactos
La generación de un artefacto se desencadena cuando se solicita al agente una nueva release. El agente, antes de generar la rama correspondiente, debe calcular la versión de la release según lo definido en el apartado de versionado y a partir de ahí, generar la rama a partir de lo que existe en 'main'. Una vez existe la rama, se debe desencadenar una pipeline que construya el artefacto:
- Para proyectos C#:
  - Se generarán los artefactos con la configuración Release, sin símbolos de depuración y usando la versión calculada.
  - Los artefactos serán comprimidos en zip (un zip por cada artefacto desplegable) y serán incluidos en la release de GitHub.
  - En la release de GitHub se deben incluir las instrucciones para configurar e instalar los artefactos.
- Para proyectos python:
  - Se generarán los artefactos correspondientes usando la versión calculada.
  - Los artefactos serán comprimidos en zip (un zip por cada artefacto desplegable) y serán incluidos en la release de GitHub.
  - En la release de GitHub se deben incluir las instrucciones para configurar e instalar los artefactos.
- Para proyectos react:
  - Se generarán los artefactos correspondientes usando la versión calculada.
  - Los artefactos serán comprimidos en zip (un zip por cada artefacto desplegable) y serán incluidos en la release de GitHub.
  - En la release de GitHub se deben incluir las instrucciones para configurar e instalar los artefactos.
## Proceso de OnBoarding
El proceso de onboarding se podrá desencadenar por uno de estos dos motivos:
1. El espacio de trabajo no es un repositorio de git.
2. El espacio de trabajo es un repositorio de git pero solo contiene el commit inicial.

El flujo del proceso de onboarding constará de los siguientes pasos:
1. Se solicitará el nombre de usuario de github para obtener el nombre completo y el correo de noreply, con el objetivo de atribuirle los cambios en el repositorio.
2. Se solicitará el nombre del repositorio.
3. Se solicitará el nombre del producto / proyecto.
4. Se solicitará la descripción del producto / proyecto.
5. Se solicitará el tipo de proyecto que va a contener el repositorio.

Una vez disponemos de toda la información necesaria:

1. Se instalarán las herramientas necesarias para el entorno (git, dotnet, python, openspec, node, npm, gh, etc.).
2. En caso de ser necesario, se debe realizar la inicialización del directorio como un repositorio git.
3. Git no puede utilizar la identidad global, por lo que el nombre y correo del usuario se configurarán como identidad local de git.
4. Si gh no dispone de una identidad válida, se le debe configurar de forma interactiva.
5. Se configurará OpenSpec (config.yaml) para que tenga en cuenta lo definido en este documento.
6. Se creará el repositorio público en GitHub si no existía previamente.
7. Se configurará el repositorio de GitHub teniendo en cuenta lo siguiente:
   - General
     - Template repository: off
   - Releases
     - Enable release immutability: on
   - Features
     - Wikis: off
     - Issues: on
       - Issue permissions: Collaborators only
     - Sponsorships: off
     - Preserve this repository: off
     - Discussions: off
     - Projects: off
     - Pull requests: on
       - Pull requests permissions: Collaborators only
   - Pull Requests
     - Allow merge commits: off
     - Allow squash merging: on
       - Default commit message: Pull request title
     - Allow rebase merging: off
     - Always suggest updating pull request branches: on
     - Allow auto-merge: off
     - Automatically delete head branches: on
   - Commits
     - Require contributors to sign off on web-based commits: on
     - Allow comments on individual commits: on
   - Archives
     - Include Git LFS objects in archives: off
   - Pushes
     - Limit how many branches and tags can be updated in a single push: off
   - Issues
     - Auto-close issues with merged linked pull requests : on
   - Code security
     - Dependency graph: on
     - Dependabot alerts: on
     - Dependabot security updates: on
     - Dependabot version updates: on
     - Secret scanning: on
     - Push protection: on
8. El repositorio debe tener 2 rulesets:
- Protección de la rama main:
  - El administrador del repositorio podrá realizar bypass de las reglas
  - La rama a proteger es main
  - La rama no se podrá borrar
  - Usuarios con permisos de «push» no podrán realizar «force push».
  - Se requiere histórico lineal
  - Se requiere PR antes de combinar cambios
    - Se requiere 1 aprobador
    - Se resetean las aprobaciones cuando se incorporan nuevos cambios
    - Se requiere aprobación de los cambios recientes
    - Se requiere que las conversaciones queden resueltas
    - Se requiere combinación con Squash
  - Se requiere escaneo de código con Code QL
    - Alertas de seguridad: alto o superior
    - Alertas: errores
  - Se requiere resultados de calidad en código:
    - Severidad: errores
  - Se requiere que pasen las comprobaciones de estado (status checks) de calidad de código (linter, formato y tipado estático), de pruebas unitarias con cobertura y de validación del título de la pull request antes de combinar cambios.
  - Si el repositorio contiene proyectos de backend, se requiere que pasen las comprobaciones de estado (status checks) de las pruebas de integración antes de combinar cambios. Esta regla no se aplica a repositorios que solo contengan proyectos de frontend.
- Protección de las ramas de release:
  - El administrador del repositorio podrá realizar bypass de las reglas
  - Las ramas a proteger siguen el patrón 'release/v*'
  - La rama no se podrá borrar
  - La rama no se podrá actualizar
  - Usuarios con permisos de «push» no podrán realizar «force push».
9. Crear el scaffolding de los proyectos, con las tecnologías indicadas.
- Los proyectos deben estar organizados en 2 directorios ubicados en la raiz del espacio de trabajo.
  - backend: aquí residirán los proyectos del backend
  - frontend: aquí residirán los proyectos del frontend
- Se crearán los workflows de GitHub Actions que se ejecutarán en cada pull request hacia main. Sus comprobaciones serán las requeridas por el ruleset de protección de main:
  - Calidad de código: linter, comprobación de formato y tipado estático de cada proyecto.
  - Pruebas unitarias con comprobación de cobertura mínima del 80%.
  - Pruebas de integración (solo si hay proyectos de backend).
  - Validación del título de la pull request según la convención de commits convencionales.
- Se creará el fichero de configuración de Dependabot (.github/dependabot.yml) para los ecosistemas de los proyectos seleccionados. Para runtimes y herramientas con ciclos LTS publicados oficialmente, las actualizaciones de versión deben limitarse a versiones de una línea LTS vigente mediante filtros compatibles con el ecosistema; las librerías sin clasificación LTS seguirán recibiendo actualizaciones normales. No se desactivarán las actualizaciones de seguridad.
10. Ajustar el fichero .gitignore para adaptarlo a los lenguajes y tecnologías seleccionadas.
11. Ajustar el fichero readme.md con la descripción y objetivos del proyecto, y los enlaces a la documentación.

> Una vez se haya completado el proceso de onboarding, el harness no se podrá modificar sin un ADR que justifique el cambio.
## Seguridad
### Controles mínimos para todos los proyectos
- **Secretos y configuración**: no incluir contraseñas, tokens, claves privadas ni cadenas de conexión con credenciales en el código, logs o repositorio. Usar variables de entorno o un gestor de secretos; proporcionar un .env.example sin valores reales. Dar a cada secreto acceso mínimo y rotarlo si se expone.
- **Dependencias y cadena de suministro**: usar versiones fijadas o gestionadas de forma reproducible, revisar vulnerabilidades y actualizar dependencias. No instalar paquetes sin justificar su origen y necesidad.
- **Validación y manejo de errores**: validar los datos en los límites de la aplicación; no exponer stack traces, secretos ni detalles internos en respuestas o mensajes de error.
- **Datos y permisos**: aplicar mínimo privilegio. Para PostgreSQL, usar cuentas distintas según función y no ejecutar la aplicación como administrador. Limitar también los permisos de RabbitMQ.
- **Comunicaciones**: usar TLS para conexiones que atraviesen redes no confiables. No registrar datos sensibles; proteger los logs y evitar incluir credenciales o información personal innecesaria.
- **Construcción y despliegue**: ejecutar análisis de código y dependencias en CI; proteger credenciales de pipelines y restringir quién puede publicar releases.
- **Pruebas**: cubrir controles de autorización, validación y manejo de fallos con pruebas relevantes; corregir vulnerabilidades críticas y altas antes de publicar.
### Controles específicos para APIs
- Las rutas de las APIs deben seguir el patrón `/api/v<num-version>/<path>` (por ejemplo, `/api/v1/auth/login`).
- Definir autenticación y autorización según los casos de uso; comprobar permisos en cada operación y recurso, no solo al iniciar sesión.
- Limitar tamaño y frecuencia de peticiones, y validar tipos, formatos y rangos de entrada.
- Evitar inyecciones SQL mediante consultas parametrizadas; proteger también el uso de comandos del sistema y rutas de archivos.
- Configurar CORS solo para los orígenes necesarios y no devolver información sensible en respuestas.
- Si se manejan contraseñas, almacenarlas con un algoritmo de hash adecuado para contraseñas, nunca en texto claro ni con cifrado reversible.
### Consolas y procesos en segundo plano
- No aceptar secretos como argumentos de línea de comandos si podrían quedar visibles en el historial o en la lista de procesos.
- Validar archivos y rutas de entrada; evitar sobrescribir o leer archivos fuera de las ubicaciones previstas.
- Para tareas programadas o consumidores de RabbitMQ, limitar permisos, controlar reintentos y evitar que mensajes inválidos provoquen bucles de procesamiento.

Como referencias, usara OWASP ASVS para requisitos de aplicaciones y OWASP API Security Top 10 para APIs. Además, cada proyecto debe evaluar amenazas y datos sensibles de su contexto: esos requisitos son una base, no sustituyen el análisis del sistema concreto.