# Spec Delta

## Purpose

Establece las condiciones para crear cuentas Lumia, verificar la identidad mediante correo electrónico y prevenir altas inválidas o no permitidas.

## ADDED Requirements

### Requirement: Datos requeridos de registro
El sistema SHALL solicitar nombre, apellidos, año de nacimiento, idioma, país, correo electrónico y contraseña para registrar una cuenta.

#### Scenario: Registro con datos completos
- **WHEN** la persona envía todos los datos requeridos con formatos válidos
- **THEN** el sistema crea la cuenta pendiente de activación

### Requirement: Restricción de edad
El sistema SHALL permitir registrarse únicamente a personas de entre 14 y 99 años, ambos inclusive, según el año de nacimiento.

#### Scenario: Edad permitida
- **WHEN** la edad calculada a partir del año de nacimiento está entre 14 y 99
- **THEN** el sistema acepta la edad como válida para el registro

#### Scenario: Edad fuera del rango
- **WHEN** la edad calculada es menor que 14 o mayor que 99
- **THEN** el sistema rechaza el registro e informa que no se cumple el rango permitido

### Requirement: Validación de contraseña
El sistema SHALL exigir una contraseña de al menos ocho caracteres que incluya minúsculas, mayúsculas, números y símbolos.

#### Scenario: Contraseña que cumple la política
- **WHEN** la contraseña contiene al menos ocho caracteres y las cuatro categorías requeridas
- **THEN** el sistema la acepta como válida para registro

#### Scenario: Contraseña que no cumple la política
- **WHEN** la contraseña no cumple la longitud o alguna categoría requerida
- **THEN** el sistema rechaza la contraseña e indica que debe cumplir la política

### Requirement: Indicador de entropía de contraseña
El sistema SHALL mostrar una estimación de la entropía de la contraseña mientras la persona la escribe y SHALL penalizar patrones predecibles.

#### Scenario: Contraseña predecible
- **WHEN** la persona escribe una contraseña predecible como `Password1`
- **THEN** el indicador refleja una entropía menor que la de una contraseña menos predecible de longitud comparable

### Requirement: Rechazo de correos temporales
El sistema SHALL impedir el registro con direcciones pertenecientes a plataformas de correo temporal.

#### Scenario: Dirección de correo temporal
- **WHEN** la persona intenta registrarse con una dirección identificada como temporal
- **THEN** el sistema rechaza el registro

### Requirement: Rechazo de cuentas bloqueadas o baneadas
El sistema SHALL impedir que un usuario bloqueado o baneado vuelva a registrarse.

#### Scenario: Cuenta no elegible para una nueva alta
- **WHEN** el registro corresponde a una cuenta bloqueada o baneada
- **THEN** el sistema rechaza el registro

### Requirement: Verificación de correo
El sistema SHALL enviar un correo de verificación al completar el registro y SHALL mantener la cuenta sin activar hasta completar la verificación.

#### Scenario: Cuenta recién registrada
- **WHEN** se completa un registro válido
- **THEN** el sistema envía el correo de verificación y no permite navegar por el área privada antes de la activación

### Requirement: Auditoría de registros correctos
El sistema SHALL registrar cada registro correcto con usuario, fecha y hora, dirección IP del cliente, tipo de dispositivo y user-agent.

#### Scenario: Registro correcto detrás de nginx
- **WHEN** un registro correcto llega a través del proxy inverso nginx
- **THEN** el registro de auditoría contiene la dirección IP del cliente y el tipo de dispositivo `tv`, `mobile`, `web` u `other`

### Requirement: Desactivación del registro
El sistema SHALL permitir desactivar el registro mediante una feature flag.

#### Scenario: Registro desactivado
- **WHEN** la feature flag de registro está desactivada
- **THEN** el sistema no crea nuevas cuentas
