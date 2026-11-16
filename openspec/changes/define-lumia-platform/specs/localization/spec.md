# Spec Delta

## Purpose

Define los idiomas disponibles y cómo se selecciona el idioma para visitantes y usuarios autenticados.

## ADDED Requirements

### Requirement: Idiomas soportados
El sistema SHALL ofrecer la interfaz en español y en inglés, utilizando español como idioma predeterminado.

#### Scenario: Idioma predeterminado
- **WHEN** no existe otra preferencia de idioma aplicable
- **THEN** el sistema muestra la interfaz en español

### Requirement: Selección de idioma en el área pública
El sistema SHALL seleccionar en el área pública el idioma del navegador cuando esté soportado y SHALL usar español si no lo está.

#### Scenario: Navegador en inglés
- **WHEN** un visitante accede con el navegador configurado en inglés
- **THEN** el área pública se muestra en inglés

#### Scenario: Navegador en idioma no soportado
- **WHEN** un visitante accede con el navegador configurado en un idioma distinto de español e inglés
- **THEN** el área pública se muestra en español

### Requirement: Preferencia de idioma en el área privada
El sistema SHALL mostrar el área privada en el idioma elegido por el usuario.

#### Scenario: Usuario elige inglés
- **WHEN** un usuario autenticado ha elegido inglés
- **THEN** el área privada se muestra en inglés

#### Scenario: Usuario elige español
- **WHEN** un usuario autenticado ha elegido español
- **THEN** el área privada se muestra en español
