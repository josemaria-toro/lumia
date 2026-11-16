# Spec Delta

## Purpose

Define las capacidades operativas para informar de mantenimientos, programar su activación y supervisar los procesos en segundo plano.

## ADDED Requirements

### Requirement: Página de mantenimiento
El sistema SHALL disponer de una página de mantenimiento para informar a los usuarios cuando se despliegue una actualización.

#### Scenario: Mantenimiento activo
- **WHEN** la página de mantenimiento está activa
- **THEN** los visitantes reciben la página informativa en lugar del acceso habitual a la plataforma

### Requirement: Programación de mantenimiento
El sistema SHALL proporcionar una página de administración desde la que se pueda programar la activación de la página de mantenimiento.

#### Scenario: Mantenimiento programado
- **WHEN** un administrador programa la activación del mantenimiento
- **THEN** el sistema activa la página en el momento programado

### Requirement: Estado de procesos en segundo plano
El sistema SHALL permitir que el administrador consulte el estado de los procesos en segundo plano.

#### Scenario: Consulta de procesos
- **WHEN** un administrador consulta los procesos en segundo plano
- **THEN** el sistema muestra el estado disponible de esos procesos

### Requirement: Dirección del cliente detrás del proxy inverso
El sistema SHALL obtener la dirección IP del cliente teniendo en cuenta que las aplicaciones se exponen a través del proxy inverso nginx.

#### Scenario: Petición a través de nginx
- **WHEN** una petición llega a la aplicación a través de nginx
- **THEN** el sistema identifica la dirección IP del cliente para los registros que la requieren

### Requirement: Comprobación de salud
El sistema SHALL ofrecer un punto de comprobación de salud que informe de si la API y su base de datos están operativas sin revelar detalles internos.

#### Scenario: Servicio operativo
- **WHEN** se consulta la comprobación de salud y la API y la base de datos responden
- **THEN** el sistema informa de que está operativo

#### Scenario: Dependencia no disponible
- **WHEN** se consulta la comprobación de salud y la base de datos no responde
- **THEN** el sistema informa de que no está operativo sin incluir detalles internos ni datos sensibles

### Requirement: Registros estructurados
El sistema SHALL generar registros estructurados de los eventos relevantes y de los errores, y NO SHALL incluir en ellos contraseñas, tokens, valores de configuración sensibles ni datos personales innecesarios.

#### Scenario: Error de aplicación
- **WHEN** se produce un error en la API o en un proceso en segundo plano
- **THEN** el sistema registra un evento estructurado con su contexto sin datos sensibles

### Requirement: Métricas de procesos en segundo plano
El sistema SHALL registrar para cada proceso en segundo plano su última ejecución, duración, resultado y elementos procesados, y SHALL permitir que el administrador las consulte junto con su estado.

#### Scenario: Consulta de métricas
- **WHEN** un administrador consulta un proceso en segundo plano
- **THEN** el sistema muestra su última ejecución, duración, resultado y elementos procesados

#### Scenario: Proceso con fallo
- **WHEN** una ejecución de un proceso en segundo plano falla
- **THEN** el sistema conserva el resultado fallido y su momento para que el administrador lo consulte

