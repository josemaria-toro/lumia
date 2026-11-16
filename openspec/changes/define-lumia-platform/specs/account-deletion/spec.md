# Spec Delta

## Purpose

Define el proceso de baja solicitado por una persona usuaria, la oportunidad de revertirlo y la eliminación posterior de la cuenta y sus datos.

## ADDED Requirements

### Requirement: Solicitud de baja desde el perfil
El sistema SHALL permitir que un usuario solicite la baja de su cuenta desde la pantalla de perfil y SHALL enviar un correo informativo sobre la solicitud.

#### Scenario: Solicitud registrada
- **WHEN** un usuario solicita la baja desde su perfil
- **THEN** el sistema registra la solicitud y envía un correo con información para revertirla

### Requirement: Reversión durante el periodo de gracia
El sistema SHALL permitir revertir la solicitud de baja durante los 15 días posteriores a la solicitud.

#### Scenario: Reversión dentro de 15 días
- **WHEN** el usuario revierte la solicitud antes de que transcurran 15 días
- **THEN** el sistema cancela la baja pendiente y mantiene la cuenta

### Requirement: Baja y borrado diferidos
El sistema SHALL dar de baja la cuenta al cumplirse 15 días desde la solicitud no revertida y SHALL borrar sus datos 30 días después de la baja.

#### Scenario: Borrado del historial de visualización
- **WHEN** se ejecuta el borrado de datos de una cuenta dada de baja
- **THEN** el sistema elimina también su historial de visualización y las posiciones de reproducción

#### Scenario: Baja no revertida
- **WHEN** transcurren 15 días desde la solicitud sin que se haya revertido
- **THEN** el sistema da de baja la cuenta y programa el borrado de sus datos para 30 días después

### Requirement: No permitir el alta antes del borrado
El sistema SHALL impedir que una cuenta dada de baja se registre de nuevo mientras sus datos no hayan sido borrados.

#### Scenario: Cuenta pendiente de borrado
- **WHEN** se intenta registrar una cuenta dada de baja cuyos datos aún existen
- **THEN** el sistema rechaza el registro
