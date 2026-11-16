# Arquitectura

- Arquitectura admitida: **hexagonal**, cumpliendo los principios **SOLID**.
- Inyección de dependencias **obligatoria por diseño**: proveedores, servicios y configuraciones se inyectan por constructor.
- La configuración se inyecta por constructor **únicamente con el patrón Options**. No se admiten parámetros de configuración sueltos en un constructor.
