# Lumia

Lumia es una plataforma para la visualización de contenido en streaming.

## Documentación

- [Arquitectura](docs/architecture.md)
- [Diagramas de clases](docs/class-diagrams.md)
- [Casos de uso](docs/use-cases.md)
- [Construcción, configuración e instalación](docs/installation.md)
- [Configuración](docs/configuration.md)
- [Decisiones de arquitectura (ADR)](docs/adr/)
- [Deuda técnica](docs/technical-debt.md)

## Objetivos

- Ofrecer el catálogo de contenido en streaming a través de una API (`backend/src/Lumia.Api`).
- Procesar tareas en segundo plano con workers de consola (`backend/src/Lumia.Workers`).
- Ofrecer una interfaz web responsiva y accesible (WCAG 2.0 AA) (`frontend/lumia-web`).

## Estructura

```
backend/    API ASP.NET Core, workers C#, dominio, aplicación, infraestructura y pruebas
frontend/   Aplicación React (Vite + TypeScript)
docs/       Documentación del proyecto
harness/    Reglas, guardarraíles y procesos de desarrollo con agentes de IA
openspec/   Especificaciones (OpenSpec)
```
