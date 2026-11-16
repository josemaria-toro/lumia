# Spec Delta

## Purpose

Permite a cada usuario autenticado conservar y gestionar una selección personal de contenidos favoritos.

## ADDED Requirements

### Requirement: Marcar contenido como favorito
El sistema SHALL permitir que un usuario autenticado marque un contenido como favorito.

#### Scenario: Marcar un contenido
- **WHEN** el usuario marca como favorito una película, serie o canal
- **THEN** el sistema conserva ese contenido en la lista de favoritos del usuario

### Requirement: Desmarcar contenido favorito
El sistema SHALL permitir que un usuario autenticado desmarque un contenido previamente marcado como favorito.

#### Scenario: Quitar un favorito
- **WHEN** el usuario desmarca un contenido de sus favoritos
- **THEN** el sistema lo elimina de la lista de favoritos de ese usuario

### Requirement: Gestionar favoritos
El sistema SHALL proporcionar una pantalla donde el usuario pueda gestionar sus contenidos favoritos.

#### Scenario: Consultar favoritos
- **WHEN** el usuario abre la pantalla de favoritos
- **THEN** el sistema muestra los contenidos que ha marcado como favoritos
