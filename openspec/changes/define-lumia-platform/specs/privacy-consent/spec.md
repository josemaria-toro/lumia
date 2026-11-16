# Spec Delta

## Purpose

Controla la aceptación de cookies y de la política de privacidad vigente, manteniendo evidencia de las políticas aceptadas por cada usuario.

## ADDED Requirements

### Requirement: Consentimiento de cookies en el área pública
El sistema SHALL mostrar la política de cookies como un popup en el área pública y SHALL requerir su aceptación antes de permitir continuar navegando.

#### Scenario: Visitante sin aceptación
- **WHEN** un visitante accede al área pública sin haber aceptado la política de cookies
- **THEN** el sistema muestra el popup y no permite continuar la navegación hasta que la acepte

#### Scenario: Política de cookies aceptada
- **WHEN** el visitante acepta la política de cookies
- **THEN** el sistema permite continuar la navegación

### Requirement: Aceptación de la última política de privacidad
El sistema SHALL comprobar después de autenticar a un usuario si ha aceptado la última política de privacidad y SHALL solicitar su aceptación cuando esté pendiente.

#### Scenario: Aceptación pendiente
- **WHEN** un usuario autenticado no ha aceptado la versión vigente de la política de privacidad
- **THEN** el sistema muestra la política y requiere su aceptación antes de continuar

#### Scenario: Versión vigente ya aceptada
- **WHEN** el usuario autenticado ya ha aceptado la última versión de la política
- **THEN** el sistema permite continuar sin volver a solicitar esa aceptación

### Requirement: Historial de políticas aceptadas
El sistema SHALL conservar un historial de las políticas de privacidad que ha aceptado cada usuario.

#### Scenario: Aceptación de una nueva versión
- **WHEN** el usuario acepta una versión nueva de la política de privacidad
- **THEN** el sistema registra esa aceptación sin eliminar el historial de versiones aceptadas anteriormente
