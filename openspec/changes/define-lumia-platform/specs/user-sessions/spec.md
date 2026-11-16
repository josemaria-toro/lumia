# Spec Delta

## Purpose

Define la identificación y vigencia de las sesiones de usuario para que el backend pueda determinar si una sesión sigue activa.

## ADDED Requirements

### Requirement: Identificación de sesión mediante cookie
El sistema SHALL crear una cookie de sesión tras una autenticación correcta y SHALL utilizarla para identificar al usuario en el backend.

#### Scenario: Sesión creada tras autenticación
- **WHEN** la autenticación del usuario se completa correctamente
- **THEN** el sistema crea la cookie de sesión y el backend puede identificar al usuario asociado

### Requirement: Comprobación de sesión activa
El backend SHALL disponer de un mecanismo para comprobar si una sesión identificada por cookie existe y está activa.

#### Scenario: Sesión activa
- **WHEN** una petición presenta una cookie asociada a una sesión vigente
- **THEN** el backend reconoce la sesión como activa

### Requirement: Expiración por inactividad
El sistema SHALL mantener la sesión durante 30 minutos desde la última actividad y SHALL extender su vigencia una vez cada cinco minutos cuando exista actividad del usuario.

#### Scenario: Actividad durante una sesión
- **WHEN** el usuario mantiene actividad en una sesión vigente
- **THEN** el sistema renueva la vigencia conforme al intervalo de cinco minutos sin superar los 30 minutos desde la actividad más reciente

#### Scenario: Inactividad durante 30 minutos
- **WHEN** transcurren 30 minutos sin actividad del usuario
- **THEN** el sistema considera expirada la sesión

### Requirement: Duración máxima de sesión
El sistema SHALL finalizar la sesión al alcanzar ocho horas desde su creación, aunque el usuario haya mantenido actividad.

#### Scenario: Límite máximo alcanzado
- **WHEN** una sesión alcanza ocho horas desde su creación
- **THEN** el sistema la finaliza y requiere una nueva autenticación

### Requirement: Navegación tras expiración
El sistema SHALL mostrar la pantalla de inicio cuando no exista una sesión o cuando esta haya expirado.

#### Scenario: Sesión inexistente o expirada
- **WHEN** el usuario navega sin una sesión activa
- **THEN** el sistema muestra la pantalla de inicio
