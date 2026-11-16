# Modelos de datos

- Tablas y columnas en **snake_case**.
- Auditoría en todas las tablas: `created_at` (obligatorio), `created_by` (opcional), `updated_at` (obligatorio), `updated_by` (opcional).
- **Sin migraciones.** Cada cambio del modelo genera un script `<yymmdd>.sql`.
- Varios cambios el mismo día → se actualiza el fichero de ese día. Lo ya definido en él **no se modifica**; los cambios se añaden **al final con `ALTER`**.
- El script incluye la creación de la base de datos (con el nombre del producto) y 3 usuarios:
  - **Administrador**: propietario de la base de datos.
  - **Aplicación**: SELECT, INSERT, UPDATE.
  - **Mantenimiento**: como la aplicación, más DELETE.
- La aplicación nunca se ejecuta como administrador.
