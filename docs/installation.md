# Construcción, configuración e instalación

## Requisitos

.NET SDK 10 (LTS), Node.js (LTS) y npm. Docker será necesario cuando se incorporen pruebas de integración con Testcontainers.

## Construcción y pruebas

```bash
# Backend
cd backend
dotnet build Lumia.sln -warnaserror
dotnet test tests/Lumia.UnitTests /p:CollectCoverage=true /p:Threshold=80 /p:ThresholdType=line
dotnet test tests/Lumia.IntegrationTests --filter "Category=Integration"

# Frontend
cd frontend/lumia-web
npm ci && npm run lint && npx prettier --check . && npx tsc --noEmit
npm run test:coverage && npm run e2e
```

Strong name: las compilaciones firmadas reciben `-p:StrongNameKeyFile=<ruta al .snk>`. La clave no se versiona; el CI genera una temporal y las releases usan el secreto `STRONG_NAME_KEY` (base64 de la clave).

## Instalación de los artefactos de una release

1. Descarga los zip de la release de GitHub (`Lumia.Api-<version>.zip`, `Lumia.Workers-<version>.zip`, `lumia-web-<version>.zip`).
2. Descomprímelos en el servidor de destino.
3. Configura las variables descritas en [configuración](configuration.md).
4. Backend: ejecuta `dotnet Lumia.Api.dll` y `dotnet Lumia.Workers.dll`. Frontend: sirve el contenido estático con un servidor web y enruta `/api` hacia la API.
