# Spec Delta

## Purpose

Establece las capacidades de reproducción audiovisual que Lumia ofrece para películas, series y canales de televisión.

## ADDED Requirements

### Requirement: Reproducción en streaming
El sistema SHALL reproducir contenidos multimedia mediante streaming.

#### Scenario: Inicio de reproducción
- **WHEN** el usuario selecciona un contenido reproducible
- **THEN** el reproductor inicia su reproducción en streaming

### Requirement: Formatos de reproducción iniciales
El sistema SHALL reproducir canales de televisión mediante HLS y películas y series en formato MP4 con vídeo H.264 y audio AAC.

#### Scenario: Reproducción de un canal
- **WHEN** el usuario inicia un canal compatible
- **THEN** el reproductor reproduce el canal mediante HLS

#### Scenario: Reproducción de una película o serie
- **WHEN** el usuario inicia un archivo MP4 con vídeo H.264 y audio AAC
- **THEN** el reproductor reproduce el archivo en streaming

### Requirement: Controles básicos del reproductor
El reproductor SHALL permitir reproducir, pausar y detener el contenido.

#### Scenario: Pausar y reanudar
- **WHEN** el usuario pausa el contenido y después selecciona reproducir
- **THEN** el reproductor pausa y reanuda la reproducción

#### Scenario: Detener contenido
- **WHEN** el usuario selecciona detener
- **THEN** el reproductor detiene la reproducción

### Requirement: Pantalla completa
El reproductor SHALL permitir visualizar el contenido a pantalla completa.

#### Scenario: Activar pantalla completa
- **WHEN** el usuario selecciona la opción de pantalla completa
- **THEN** el contenido se presenta a pantalla completa

### Requirement: Siguiente episodio o canal
El reproductor SHALL permitir pasar al siguiente capítulo de una serie o al siguiente canal de televisión.

#### Scenario: Siguiente capítulo
- **WHEN** se reproduce un capítulo de una serie y el usuario solicita avanzar al siguiente
- **THEN** el reproductor inicia el siguiente capítulo disponible

#### Scenario: Siguiente canal
- **WHEN** se reproduce un canal y el usuario solicita avanzar al siguiente
- **THEN** el reproductor cambia al siguiente canal disponible

### Requirement: Carrusel de canales
El reproductor SHALL ofrecer un carrusel para cambiar entre canales de televisión.

#### Scenario: Selección desde el carrusel
- **WHEN** el usuario selecciona otro canal en el carrusel
- **THEN** el reproductor cambia la reproducción al canal seleccionado

### Requirement: Reproducción restringida a usuarios registrados y activos
El sistema SHALL permitir la reproducción de cualquier contenido, incluidos los canales de televisión, únicamente a usuarios registrados cuya cuenta esté activa, y NO SHALL exponer rutas de archivos del servidor.

#### Scenario: Usuario registrado y activo
- **WHEN** un usuario autenticado con cuenta activa inicia la reproducción de un contenido
- **THEN** el sistema entrega el flujo de reproducción

#### Scenario: Visitante sin sesión
- **WHEN** una persona no autenticada solicita la reproducción de un contenido o el acceso directo a su flujo
- **THEN** el sistema deniega el acceso

#### Scenario: Cuenta no activa
- **WHEN** un usuario cuya cuenta no está activa solicita la reproducción de un contenido
- **THEN** el sistema deniega el acceso

#### Scenario: Sesión expirada durante la reproducción
- **WHEN** la sesión del usuario expira y el reproductor solicita más datos del flujo
- **THEN** el sistema deniega la entrega y la aplicación redirige al usuario al inicio

### Requirement: Subtítulos opcionales
El reproductor SHALL ofrecer la opción de activar subtítulos únicamente cuando existan ficheros de subtítulos asociados al contenido, y SHALL permitir desactivarlos.

#### Scenario: Contenido con subtítulos
- **WHEN** un usuario reproduce un contenido que tiene ficheros de subtítulos asociados
- **THEN** el reproductor ofrece seleccionar uno de los subtítulos disponibles o desactivarlos

#### Scenario: Contenido sin subtítulos
- **WHEN** un usuario reproduce un contenido sin ficheros de subtítulos asociados
- **THEN** el reproductor no muestra la opción de subtítulos

### Requirement: Reproducción en Chromecast
El reproductor SHALL permitir enviar la reproducción de un contenido a un dispositivo Chromecast de la red del usuario, controlarla desde la aplicación y volver a reproducirla en el navegador.

#### Scenario: Envío a Chromecast
- **WHEN** un usuario autenticado con cuenta activa selecciona un dispositivo Chromecast disponible
- **THEN** el contenido se reproduce en ese dispositivo y el usuario puede reproducir, pausar y detener desde la aplicación

#### Scenario: Acceso temporal del dispositivo
- **WHEN** un dispositivo Chromecast solicita el flujo de un contenido enviado por un usuario autorizado
- **THEN** el sistema lo entrega mientras el permiso temporal concedido a esa reproducción siga vigente y deniega cualquier otra petición sin ese permiso

#### Scenario: Permiso temporal caducado
- **WHEN** el permiso temporal de una reproducción en Chromecast caduca o el usuario deja de estar activo
- **THEN** el sistema deja de entregar el flujo a ese dispositivo

#### Scenario: Volver al navegador
- **WHEN** el usuario detiene el envío a Chromecast
- **THEN** la reproducción continúa en el navegador desde la posición actual
