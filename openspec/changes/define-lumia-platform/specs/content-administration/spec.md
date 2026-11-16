# Spec Delta

## Purpose

Define las operaciones administrativas sobre contenidos y la asignación de permisos de administración por usuario, acción y tipo de contenido.

## ADDED Requirements

### Requirement: Roles disponibles
El sistema SHALL disponer de exactamente dos roles de administración: administrador y colaborador.

#### Scenario: Roles del sistema
- **WHEN** se consulta la lista de roles disponibles para la administración
- **THEN** el sistema ofrece administrador y colaborador

### Requirement: Acceso a administración basado en roles
El sistema SHALL permitir acceder al área de administración únicamente a usuarios que tengan un rol administrativo asignado.

#### Scenario: Usuario con rol
- **WHEN** un usuario con un rol asignado accede al área de administración
- **THEN** el sistema permite el acceso conforme a los permisos de su rol

#### Scenario: Usuario sin rol
- **WHEN** un usuario sin rol intenta acceder al área de administración
- **THEN** el sistema deniega el acceso

### Requirement: Rol de administrador
El sistema SHALL permitir que el rol de administrador realice operaciones de creación, lectura, actualización y borrado sobre todas las entidades y asigne roles a otros usuarios.

#### Scenario: Administrador gestiona una entidad
- **WHEN** un administrador realiza una operación CRUD sobre una entidad
- **THEN** el sistema permite la operación

#### Scenario: Administrador asigna un rol
- **WHEN** un administrador asigna un rol a otro usuario
- **THEN** el sistema registra la asignación y aplica el rol al usuario

### Requirement: Rol de colaborador
El sistema SHALL permitir que el rol de colaborador lea y actualice contenidos autorizados y SHALL impedirle gestionar roles o permisos.

#### Scenario: Colaborador actualiza contenido autorizado
- **WHEN** un colaborador actualiza un contenido para el que tiene permiso
- **THEN** el sistema aplica la actualización

#### Scenario: Colaborador intenta gestionar permisos
- **WHEN** un colaborador intenta asignar roles o modificar permisos
- **THEN** el sistema deniega la operación

### Requirement: Permisos de grano fino
El sistema SHALL permitir definir permisos de acceso, lectura y actualización por usuario o rol, operación y tipo de contenido, incluidos películas, series y canales de televisión.

#### Scenario: Permiso limitado a películas
- **WHEN** un colaborador tiene permisos de actualización para películas, pero no para series
- **THEN** el sistema permite actualizar películas y deniega la actualización de series

#### Scenario: Operación no autorizada
- **WHEN** un usuario con rol intenta una operación o acceso a un tipo de contenido no permitido
- **THEN** el sistema deniega la operación o el acceso

### Requirement: Selección de correspondencia de metadatos
El sistema SHALL permitir que un usuario autorizado vuelva a elegir la correspondencia de metadatos externos asociada a un contenido.

#### Scenario: Correspondencia externa incorrecta
- **WHEN** un usuario autorizado selecciona otra correspondencia de metadatos para un contenido
- **THEN** el sistema actualiza la asociación de metadatos de ese contenido
