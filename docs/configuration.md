# Configuración

Orígenes admitidos: variables de entorno, ficheros (json, ini, xml), ficheros de secretos y base de datos. Actualmente se usan variables de entorno y `appsettings.json` (el resto está soportado por el host de .NET y se añadirá según se necesite).

| Clave | Variable de entorno | Descripción |
|:------|:--------------------|:------------|
| `Catalog:Titles` | `Catalog__Titles__0`, `Catalog__Titles__1`… | Títulos del catálogo en memoria (`CatalogOptions`) |
| `ASPNETCORE_ENVIRONMENT` | `ASPNETCORE_ENVIRONMENT` | Entorno de ejecución |

Los secretos nunca se versionan; el fichero `.env.example` no contiene valores reales.
