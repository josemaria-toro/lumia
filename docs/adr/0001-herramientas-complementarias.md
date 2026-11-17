---
harness-change: false
---
# ADR-0001: Herramientas y versiones complementarias a la tabla de tecnologías

- **Estado**: aceptado
- **Fecha**: 2026-11-16

## Contexto

La tabla de tecnologías admitidas no cubre algunas librerías necesarias para aplicar las herramientas indicadas, y algunas versiones han requerido ajustes.

## Decisión

- **Frontend**: `jsdom` y `@testing-library/*` (pruebas de componentes con Vitest), `eslint-plugin-jsx-a11y` (accesibilidad, WCAG 2.0 AA), `typescript-eslint` y `eslint-plugin-react-hooks` (reglas de ESLint), Vite (empaquetado).
- **Backend**: `Microsoft.AspNetCore.Mvc.Testing` (pruebas de integración de la API en proceso) y `coverlet.msbuild` (Coverlet con umbral de cobertura).
- **Versiones**: ESLint 9 (limitado por `eslint-plugin-jsx-a11y`), TypeScript 6.0 (limitado por `typescript-eslint`), paquetes `Microsoft.*` en 10.0.x (línea LTS de .NET).
- **Pruebas de integración**: de momento usan `WebApplicationFactory` porque aún no hay PostgreSQL ni RabbitMQ; Testcontainers se incorporará cuando existan.

## Consecuencias

Dependabot ignora las actualizaciones mayores de `Microsoft.Extensions.*`, `Microsoft.AspNetCore.*` y `@types/node`. Hay que revisar ESLint y TypeScript cuando los plugins amplíen su compatibilidad.

El alerta de seguridad de `minimatch` (dependencia transitiva de `typescript-eslint`) se resuelve con `overrides` en `package.json` hacia `minimatch` 11.x solo para `@typescript-eslint/typescript-estree`; puede retirarse cuando `typescript-eslint` actualice su dependencia.
