# Estilo de código por lenguaje

## Reglas comunes (Python, C# y React)
- Código y comentarios/documentación del código en **inglés**.
- Organización de clases: miembros de clase → constructores y métodos especiales → propiedades → métodos.
- Propiedades y métodos en **orden alfabético**, públicos primero y el resto después.

## Python (backend: consola, servicios, APIs)
- PEP 8.
- En `__init__.py`, importaciones con **rutas relativas**; en el resto de ficheros, **rutas absolutas**.
- Siempre con **entorno virtual** (`.venv`); nunca `pip install` global.

## C# (backend: consola, servicios, APIs)
- Normas de Microsoft.
- Proyectos firmados con **strong name**: claves generadas temporalmente; la clave privada se configura como variable de entorno/secreto en GitHub. **No se puede instalar mono.**

## React (frontend web)
- Guía oficial de React.
- Responsivo y accesible **WCAG 2.0 AA**.
