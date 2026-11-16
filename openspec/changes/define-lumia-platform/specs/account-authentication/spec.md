# Spec Delta

## Purpose

Define cómo se autentican los usuarios y cómo se controlan las cuentas no disponibles, la recuperación de acceso y la trazabilidad de los inicios de sesión.

## ADDED Requirements

### Requirement: Inicio de sesión con credenciales
El sistema SHALL permitir que un usuario no autenticado inicie sesión mediante su correo electrónico y contraseña.

#### Scenario: Credenciales válidas
- **WHEN** un usuario activo proporciona credenciales correctas
- **THEN** el sistema autentica al usuario y registra el acceso correcto

### Requirement: Rechazo de cuentas bloqueadas o baneadas
El sistema SHALL impedir el inicio de sesión de cuentas bloqueadas o baneadas.

#### Scenario: Cuenta no habilitada
- **WHEN** un usuario bloqueado o baneado intenta autenticarse
- **THEN** el sistema deniega el acceso

### Requirement: Bloqueo por intentos fallidos
El sistema SHALL bloquear una cuenta tras tres intentos de inicio de sesión fallidos y enviar un correo con información para recuperar la contraseña.

#### Scenario: Tercer intento fallido
- **WHEN** se produce el tercer intento fallido de una cuenta
- **THEN** el sistema bloquea la cuenta y envía el correo de recuperación

### Requirement: Activación obligatoria antes de navegar
El sistema SHALL impedir el acceso al resto de la plataforma a una cuenta registrada que todavía no haya sido activada.

#### Scenario: Cuenta pendiente de activación
- **WHEN** una cuenta no activada intenta iniciar sesión
- **THEN** el sistema muestra un aviso de activación y permite reenviar el correo de activación sin conceder acceso al resto de la plataforma

### Requirement: Recuperación de contraseña
El sistema SHALL permitir que un usuario activo solicite un cambio de contraseña mediante un token enviado por correo electrónico que vence a los 30 minutos.

#### Scenario: Token vigente
- **WHEN** el usuario presenta un token válido antes de que transcurran 30 minutos
- **THEN** el sistema permite establecer una nueva contraseña

#### Scenario: Token vencido
- **WHEN** el usuario presenta el token después de 30 minutos
- **THEN** el sistema rechaza el cambio de contraseña

### Requirement: Auditoría de accesos correctos
El sistema SHALL registrar cada inicio de sesión correcto con usuario, fecha y hora, dirección IP del cliente, tipo de dispositivo y user-agent.

#### Scenario: Acceso correcto detrás de nginx
- **WHEN** un inicio de sesión correcto llega a través del proxy inverso nginx
- **THEN** el registro contiene la dirección IP del cliente y el tipo de dispositivo `tv`, `mobile`, `web` u `other`, además del resto de los datos de auditoría

### Requirement: Desactivación del inicio de sesión
El sistema SHALL permitir desactivar el inicio de sesión mediante una feature flag.

#### Scenario: Inicio de sesión desactivado
- **WHEN** la feature flag de inicio de sesión está desactivada
- **THEN** el sistema no permite iniciar sesión
