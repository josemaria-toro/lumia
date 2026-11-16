# Spec Delta

## Purpose

Permite a visitantes y usuarios encontrar contenidos desde las pantallas de inicio y explorar el catálogo de forma organizada.

## ADDED Requirements

### Requirement: Inicio público
El sistema SHALL ofrecer una pantalla de inicio pública con un fondo visual y opciones para iniciar sesión o registrarse en la parte superior derecha.

#### Scenario: Visitante abre el inicio
- **WHEN** una persona no autenticada accede a la pantalla de inicio
- **THEN** ve el fondo público y las opciones de inicio de sesión y registro en la parte superior derecha

### Requirement: Inicio privado por tipo de contenido
El sistema SHALL mostrar a los usuarios autenticados series, películas y canales de televisión organizados por tipo de contenido.

#### Scenario: Usuario autenticado abre el inicio
- **WHEN** un usuario autenticado accede a la pantalla de inicio privada
- **THEN** el catálogo presenta series, películas y canales de televisión agrupados por tipo

### Requirement: Filtrado por tipo de contenido
El sistema SHALL proporcionar en el área privada una botonera superior para filtrar el catálogo por tipo de contenido.

#### Scenario: Filtrado de películas
- **WHEN** el usuario selecciona el filtro de películas
- **THEN** el catálogo muestra contenidos del tipo película

### Requirement: Búsqueda de contenidos
El sistema SHALL permitir a los usuarios autenticados buscar contenidos por texto en el catálogo, ignorando mayúsculas y acentos, y SHALL poder combinar la búsqueda con el filtro por tipo.

#### Scenario: Búsqueda con resultados
- **WHEN** un usuario introduce un texto que coincide con el título de uno o varios contenidos
- **THEN** el sistema muestra los contenidos coincidentes mediante tarjetas informativas y paginación dinámica

#### Scenario: Búsqueda sin resultados
- **WHEN** un usuario busca un texto que no coincide con ningún contenido
- **THEN** el sistema informa de que no hay resultados

#### Scenario: Búsqueda combinada con el filtro
- **WHEN** un usuario busca un texto con un filtro por tipo seleccionado
- **THEN** el sistema muestra solo los resultados de ese tipo

#### Scenario: Búsqueda sin sesión
- **WHEN** una persona no autenticada solicita una búsqueda en el catálogo
- **THEN** el sistema deniega la operación

### Requirement: Tarjetas informativas
El sistema SHALL mostrar contenidos mediante componentes de tarjeta que presenten información del contenido.

#### Scenario: Contenido en el catálogo
- **WHEN** un contenido aparece en una lista del catálogo
- **THEN** se muestra mediante una tarjeta informativa asociada a ese contenido

### Requirement: Paginación dinámica por scroll
El sistema SHALL presentar el contenido de forma paginada y SHALL cargar páginas adicionales dinámicamente al desplazarse por la lista.

#### Scenario: Desplazamiento hasta el final de una página
- **WHEN** el usuario se desplaza hasta el final del contenido cargado y existen más resultados
- **THEN** el sistema carga y muestra la siguiente página sin requerir una navegación manual a otra página
