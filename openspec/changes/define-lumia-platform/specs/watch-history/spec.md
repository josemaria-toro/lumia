# Spec Delta

## Purpose

Permite a cada usuario retomar sus reproducciones, conocer qué ha visto y gestionar su propio historial de visualización.

## ADDED Requirements

### Requirement: Registro de la posición de reproducción
El sistema SHALL registrar la posición de reproducción de cada película y episodio para el usuario autenticado mientras reproduce el contenido, y NO SHALL registrarla para canales de televisión.

#### Scenario: Reproducción en curso
- **WHEN** un usuario reproduce una película o un episodio
- **THEN** el sistema guarda periódicamente su posición de reproducción asociada a ese usuario y contenido

#### Scenario: Canal de televisión
- **WHEN** un usuario reproduce un canal de televisión
- **THEN** el sistema no registra posición de reproducción

### Requirement: Reanudar la reproducción
El sistema SHALL reanudar una película o episodio desde la última posición registrada del usuario.

#### Scenario: Contenido con posición guardada
- **WHEN** un usuario inicia un contenido para el que tiene una posición guardada y no visto por completo
- **THEN** el reproductor continúa desde esa posición

#### Scenario: Contenido sin posición guardada
- **WHEN** un usuario inicia un contenido sin posición guardada
- **THEN** el reproductor comienza desde el principio

### Requirement: Continuar viendo
El sistema SHALL mostrar en el inicio privado una sección de contenidos que el usuario tiene empezados y no ha terminado, ordenados del más reciente al más antiguo.

#### Scenario: Contenidos empezados
- **WHEN** un usuario con contenidos a medias accede al inicio privado
- **THEN** ve la sección de continuar viendo con esos contenidos y puede retomarlos

#### Scenario: Sin contenidos empezados
- **WHEN** un usuario sin contenidos a medias accede al inicio privado
- **THEN** la sección de continuar viendo no se muestra

### Requirement: Contenido visto
El sistema SHALL marcar un contenido como visto cuando la reproducción alcance el umbral de finalización configurado, y SHALL retirarlo de la sección de continuar viendo.

#### Scenario: Reproducción completada
- **WHEN** un usuario alcanza el umbral de finalización de una película o episodio
- **THEN** el sistema lo marca como visto y deja de ofrecerlo para continuar

### Requirement: Siguiente episodio de una serie
El sistema SHALL ofrecer en continuar viendo el siguiente episodio de una serie cuando el usuario haya terminado el anterior y exista otro episodio disponible.

#### Scenario: Episodio terminado con más episodios
- **WHEN** un usuario marca como visto un episodio y la serie tiene un siguiente episodio
- **THEN** el sistema ofrece ese siguiente episodio en continuar viendo

### Requirement: Gestión del historial propio
El sistema SHALL permitir que cada usuario elimine elementos de su historial de visualización o lo vacíe por completo, y SHALL permitir consultarlo y modificarlo únicamente a su propietario.

#### Scenario: Eliminación de un elemento
- **WHEN** un usuario elimina un elemento de su historial
- **THEN** el sistema borra su posición y estado de visto de ese contenido

#### Scenario: Historial de otro usuario
- **WHEN** un usuario intenta consultar o modificar el historial de otro usuario
- **THEN** el sistema deniega la operación
