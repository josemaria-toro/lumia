# Spec Delta

## Purpose

Define de dónde obtiene el sistema su configuración, cómo se protege la información sensible y cuándo se aplican los cambios.

## ADDED Requirements

### Requirement: Proveedores de configuración
El sistema SHALL obtener su configuración de cuatro proveedores: variables de entorno, ficheros JSON, ficheros de secretos y base de datos. Los componentes recibirán la configuración ya resuelta mediante el patrón Options.

#### Scenario: Proveedores disponibles
- **WHEN** un servicio del sistema arranca
- **THEN** compone su configuración a partir de ficheros JSON, variables de entorno, ficheros de secretos y base de datos, y no utiliza otros orígenes

#### Scenario: Formatos de fichero no soportados
- **WHEN** se proporciona un fichero de configuración en formato ini o xml
- **THEN** el sistema no lo lee como origen de configuración

### Requirement: Cadena de conexión en un fichero de secretos
El sistema SHALL leer la cadena de conexión a la base de datos únicamente de un fichero de secretos, y NO SHALL almacenarla en la base de datos ni en variables de entorno o ficheros JSON.

#### Scenario: Cadena de conexión
- **WHEN** un servicio necesita conectarse a la base de datos
- **THEN** obtiene la cadena de conexión del fichero de secretos antes de cargar el proveedor de base de datos

#### Scenario: Cadena de conexión ausente
- **WHEN** el fichero de secretos de la cadena de conexión no existe o no la contiene
- **THEN** el servicio no arranca e informa del error sin mostrar valores sensibles

### Requirement: Configuración funcional en base de datos
El sistema SHALL gestionar en base de datos toda la configuración, excepto la cadena de conexión y los valores mínimos de arranque necesarios para acceder a ella (como la clave de cifrado de los valores sensibles, ubicada en un fichero de secretos), incluidas las feature flags, las rutas y países de ingestión, los parámetros de correo y las plataformas de metadatos.

#### Scenario: Valor definido en base de datos
- **WHEN** un servicio arranca y existe un valor de configuración en la base de datos
- **THEN** el servicio utiliza ese valor

#### Scenario: Prioridad de los proveedores
- **WHEN** una misma clave está definida en ficheros JSON, variables de entorno y base de datos
- **THEN** prevalece la base de datos, después las variables de entorno y por último los ficheros JSON

#### Scenario: Valores de los ficheros de secretos
- **WHEN** el sistema compone su configuración
- **THEN** la cadena de conexión y la clave de cifrado proceden solo de ficheros de secretos y no pueden redefinirse desde la base de datos

### Requirement: Carga al iniciar
El sistema SHALL cargar el proveedor de base de datos una sola vez al iniciar cada servicio, tanto la API como los procesos en segundo plano.

#### Scenario: Carga al arrancar
- **WHEN** arranca la API o el trabajador de procesos en segundo plano
- **THEN** la configuración de base de datos queda cargada antes de atender peticiones o ejecutar tareas

#### Scenario: Base de datos no disponible al arrancar
- **WHEN** el proveedor de base de datos no puede cargar la configuración durante el arranque
- **THEN** el servicio no arranca y registra el error sin datos sensibles

#### Scenario: Cambio de configuración
- **WHEN** se modifica un valor de configuración en la base de datos con un servicio en ejecución
- **THEN** el servicio sigue usando el valor cargado hasta su siguiente reinicio

### Requirement: Valores sensibles cifrados
El sistema SHALL almacenar cifrados en la base de datos los valores de configuración sensibles, como contraseñas y claves de API, y SHALL obtener la clave de cifrado únicamente de un fichero de secretos, que puede ser distinto del de la cadena de conexión.

#### Scenario: Almacenamiento de un valor sensible
- **WHEN** se guarda un valor de configuración marcado como sensible
- **THEN** la base de datos conserva solo su valor cifrado

#### Scenario: Valor sensible no expuesto
- **WHEN** el sistema registra eventos, errores o respuestas que afectan a la configuración
- **THEN** no incluye valores sensibles en claro

#### Scenario: Clave de cifrado ausente
- **WHEN** existen valores sensibles en la base de datos y el fichero de secretos de la clave de cifrado no existe o no la contiene
- **THEN** el servicio no arranca

### Requirement: Esquema de configuración auditable
La configuración almacenada SHALL conservar la fecha de creación y de modificación de cada valor y SHALL tener nombres de tablas y columnas en `snake_case`.

#### Scenario: Registro de modificación
- **WHEN** se modifica un valor de configuración
- **THEN** se actualiza su fecha de modificación
