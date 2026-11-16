# Spec Delta

## Purpose

Define cómo se descubren los archivos multimedia, cómo se relacionan con sus metadatos y cómo se actualiza el catálogo de canales de televisión.

## ADDED Requirements

### Requirement: Rutas configurables por tipo
El sistema SHALL permitir configurar una ruta de detección para cada tipo de contenido multimedia gestionado.

#### Scenario: Ruta configurada
- **WHEN** se ejecuta la detección de contenidos
- **THEN** el sistema busca cada tipo de contenido en su ruta configurada

### Requirement: Detección periódica de películas
El sistema SHALL revisar cada 30 minutos la ruta de películas y detectar cambios en los archivos encontrados.

#### Scenario: Cambio en una carpeta de películas
- **WHEN** la revisión periódica detecta un archivo nuevo o modificado
- **THEN** el sistema incorpora o actualiza la referencia de ese archivo en el catálogo

### Requirement: Organización de películas
El sistema SHALL admitir películas organizadas en carpetas y SHALL permitir que una carpeta contenga más de un archivo de película.

#### Scenario: Varios archivos de película en una carpeta
- **WHEN** una carpeta contiene más de un archivo de película
- **THEN** el sistema detecta cada archivo como una referencia multimedia independiente

### Requirement: Detección periódica de series
El sistema SHALL revisar cada 30 minutos la ruta de series y detectar cambios en los archivos encontrados.

#### Scenario: Cambio en una carpeta de series
- **WHEN** la revisión periódica detecta un archivo nuevo o modificado
- **THEN** el sistema incorpora o actualiza la referencia de ese archivo en el catálogo

### Requirement: Organización de series por temporadas
El sistema SHALL admitir series organizadas en carpetas que contengan temporadas.

#### Scenario: Archivos dentro de temporadas
- **WHEN** los archivos de una serie están organizados en carpetas de temporadas
- **THEN** el catálogo conserva la asociación de esos archivos con la serie y su estructura de temporadas

### Requirement: Asociación de metadatos y archivos físicos
El sistema SHALL almacenar los metadatos de películas y series en la base de datos junto con una referencia al archivo físico correspondiente.

#### Scenario: Archivo asociado a metadatos
- **WHEN** un archivo de película o serie se incorpora al catálogo
- **THEN** el sistema conserva sus metadatos y la referencia al archivo físico asociado

### Requirement: Consulta configurable de metadatos
El sistema SHALL permitir consultar IMDb y TMDB para obtener información de películas y series, y SHALL permitir configurar otras plataformas externas.

#### Scenario: Consulta de metadatos
- **WHEN** el sistema procesa un contenido sin metadatos asociados
- **THEN** obtiene información de IMDb o TMDB y la asocia al contenido

#### Scenario: Plataforma externa adicional
- **WHEN** se configura una plataforma de metadatos adicional
- **THEN** el sistema puede consultarla para obtener información de películas o series

### Requirement: Actualización de canales de televisión
El sistema SHALL descargar las listas IPTV de los países configurados desde el directorio `streams` del repositorio `iptv-org/iptv` en GitHub, cargar los contenidos al catálogo persistido y SHALL refrescarlos una vez al día.

#### Scenario: Refresco diario de canales
- **WHEN** se ejecuta el ciclo diario de actualización de televisión
- **THEN** el sistema descarga las listas de los países configurados y actualiza el catálogo de canales

#### Scenario: Configuración de países IPTV
- **WHEN** se modifica la configuración de países para la ingestión IPTV y el trabajador se reinicia
- **THEN** las siguientes descargas incluyen las listas de los países configurados

### Requirement: Detección de subtítulos
El sistema SHALL detectar los ficheros de subtítulos SRT y WebVTT que acompañen a un archivo de película o episodio, identificados por tener el mismo nombre base, y SHALL asociarlos a ese contenido.

#### Scenario: Subtítulos junto al vídeo
- **WHEN** la revisión periódica encuentra un fichero de subtítulos con el mismo nombre base que un archivo de vídeo
- **THEN** el sistema asocia esos subtítulos al contenido

#### Scenario: Subtítulos eliminados
- **WHEN** un fichero de subtítulos asociado deja de existir
- **THEN** el sistema elimina su asociación con el contenido

